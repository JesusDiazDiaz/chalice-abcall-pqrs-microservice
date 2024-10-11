import boto3, logging, re
from chalice import Chalice, BadRequestError
"""from chalicelib.src.modules.application.commands.create_incident import CreateIncidentCommand
from chalicelib.src.modules.infrastructure.dto import Base
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.config.db import init_db, engine
from chalicelib.src.seedwork.application.queries import execute_query
from chalicelib.src.modules.application.queries.get_incidents import GetIncidentsQuery"""


app = Chalice(app_name='abcall-pqrs-microservice')
app.debug = True

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')

init_db()

cognito_client = boto3.client('cognito-idp')

USER_POOL_ID = 'tu_user_pool_id'
CLIENT_ID = 'tu_client_id'


@app.route('/users/{cliente_id}', methods=['GET'])
def index(client_id):
    if client_id is None:
        client_id = ""

    query_result = execute_query(GetUsersQuery(client_id))
    return query_result.result


@app.route('/users', methods=['POST'])
def incidence_post():
    user_as_json = app.current_request.json_body

    LOGGER.info("Receive create user request")
    required_fields = ["client_id", "document_type", "id_number", "name", "last_name", "email", "cellphone", "password"]
    for field in required_fields:
        if field not in user_as_json:
            raise BadRequestError(f"Missing required field: {field}")

    valid_types = ["petition", "claim"]
    if user_as_json["document_type"] not in valid_types:
        raise BadRequestError(f"Invalid 'type' value. Must be one of {valid_types}")

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, user_as_json["email"]):
        raise BadRequestError("Invalid email format")

    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=user_as_json["email"],
            Password=user_as_json["password"],  # Esto debe cumplir las políticas de Cognito
            UserAttributes=[
                {'Name': 'email', 'Value': user_as_json["email"]},
                {'Name': 'phone_number', 'Value': user_as_json["cellphone"]},
                {'Name': 'given_name', 'Value': user_as_json["name"]},
                {'Name': 'family_name', 'Value': user_as_json["last_name"]},
            ]
        )
    except cognito_client.exceptions.UsernameExistsException:
        raise BadRequestError("The email is already registered.")
    except Exception as e:
        LOGGER.error(f"Error creating user in Cognito: {str(e)}")
        raise BadRequestError("Failed to create user in Cognito.")

    cognito_user_sub = response['UserSub']

    command = CreateUserCommand(
        cognito_user_sub=cognito_user_sub,
        document_type=user_as_json["document_type"],
        client_id=user_as_json["client_id"],
        id_number=user_as_json["id_number"],
        name=user_as_json["name"],
        last_name=user_as_json["last_name"],
    )

    execute_command(command)

    return {'status': "ok", 'message': "User created successfully", 'cognito_user_sub': cognito_user_sub}



@app.route('/migrate', methods=['POST'])
def migrate():
    try:
        Base.metadata.create_all(bind=engine)
        return {"message": "Tablas creadas con éxito"}
    except Exception as e:
        return {"error": str(e)}