import boto3, logging, re
from chalice import Chalice, BadRequestError
from chalicelib.src.modules.application.commands.create_user import CreateUserCommand
from chalicelib.src.modules.application.commands.update_user import UpdateUserCommand
from chalicelib.src.modules.application.commands.delete_user import DeleteUserCommand
from chalicelib.src.modules.infrastructure.dto import Base
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.config.db import init_db, engine
from chalicelib.src.seedwork.application.queries import execute_query
from chalicelib.src.modules.application.queries.get_users import GetUsersQuery
from chalicelib.src.modules.application.queries.get_user import GetUserQuery



app = Chalice(app_name='abcall-users-microservice')
app.debug = True

LOGGER = logging.getLogger('abcall-users-microservice')

init_db()

cognito_client = boto3.client('cognito-idp')

USER_POOL_ID = 'us-east-1_YDIpg1HiU'
CLIENT_ID = '65sbvtotc1hssqecgusj1p3f9g'


@app.route('/users/{cliente_id}', methods=['GET'])
def index(client_id):
    if client_id is None:
        client_id = ""

    query_result = execute_query(GetUsersQuery(client_id=client_id))
    return query_result.result


@app.route('/user/{user_sub}', methods=['GET'])
def user_get(user_sub):
    if not user_sub:
        return {'status': 'fail', 'message': 'Invalid user subscription'}, 400

    try:
        query_result = execute_query(GetUserQuery(user_sub=user_sub))
        if not query_result.result:  # Verificar si se encontró un resultado
            return {'status': 'fail', 'message': 'User not found'}

        return {'status': 'success', 'data': query_result.result}, 200

    except Exception as e:
        LOGGER.error(f"Error fetching user: {str(e)}")
        return {'status': 'fail', 'message': 'An error occurred while fetching the user'}, 500

@app.route('/user/{user_sub}', methods=['DELETE'])
def user_delete(user_sub):
    if not user_sub:
        return {'status': 'fail', 'message': 'Invalid user subscription'}, 400

    command = DeleteUserCommand(cognito_user_sub=user_sub)

    try:
        execute_command(command)
        return {'status': 'success'}, 200

    except Exception as e:
        LOGGER.error(f"Error fetching user: {str(e)}")
        return {'status': 'fail', 'message': 'An error occurred while deleting the user'}, 400

@app.route('/user/{user_sub}', methods=['PUT'])
def user_update(user_sub):
    if not user_sub:
        return {'status': 'fail', 'message': 'Invalid user subscription'}, 400

    command = UpdateUserCommand(cognito_user_sub=user_sub, user_data=app.current_request.json_body)

    try:
        execute_command(command)
        return {'status': 'success'}, 200

    except Exception as e:
        LOGGER.error(f"Error fetching user: {str(e)}")
        return {'status': 'fail', 'message': 'An error occurred while fetching the user'}, 400


@app.route('/users', methods=['POST'])
def user_post():
    user_as_json = app.current_request.json_body

    LOGGER.info("Receive create user request")
    required_fields = ["client_id", "document_type", "user_role", "id_number", "name", "last_name", "email", "cellphone",
                       "password", "communication_type"]
    for field in required_fields:
        if field not in user_as_json:
            raise BadRequestError(f"Missing required field: {field}")

    valid_types = ["cedula", "passport", "cedula_extranjeria"]
    if user_as_json["document_type"] not in valid_types:
        raise BadRequestError(f"Invalid 'type' value. Must be one of {valid_types}")

    valid_types = ['superadmin', 'admin', 'agent', 'regular']
    if user_as_json["user_role"] not in valid_types:
        raise BadRequestError(f"Invalid 'type' value. Must be one of {valid_types}")

    valid_types = ['email', 'phone', 'sms', 'chat']
    if user_as_json["communication_type"] not in valid_types:
        raise BadRequestError(f"Invalid 'communication type' value. Must be one of {valid_types}")

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, user_as_json["email"]):
        raise BadRequestError("Invalid email format")

    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=user_as_json["email"],
            Password=user_as_json["password"],
            UserAttributes=[
                {'Name': 'custom:userRol', 'Value': user_as_json["user_rol"]}
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
        communication_type=user_as_json["communication_type"],
        user_role=user_as_json["user_role"]
    )

    execute_command(command)

    return {'status': "ok", 'message': "User created successfully", 'cognito_user_sub': cognito_user_sub}, 200

@app.route('/user/me', methods=['GET'], authorizer=app.authorizer())
def get_current_user():
    request = app.current_request
    auth_header = request.headers.get('Authorization')


    if not auth_header:
        raise BadRequestError("Missing Authorization header")

    token = auth_header.split()[1]

    try:
        user_info = cognito_client.get_user(AccessToken=token)

        user_sub = user_info['Username']

        cognito_data = {
            'username': user_info['Username'],
            'email': next(attr['Value'] for attr in user_info['UserAttributes'] if attr['Name'] == 'email'),
            'user_rol': next(attr['Value'] for attr in user_info['UserAttributes'] if attr['Name'] == 'custom:userRol'),
        }

        query_result = execute_query(GetUserQuery(user_sub=user_sub))

        if not query_result.result:  # Verificamos si se encontró un resultado en la base de datos
            return {'status': 'fail', 'message': 'User not found in database'}, 404

        user_data = {
            **cognito_data,
            **query_result.result
        }

        return {'status': 'success', 'data': user_data}, 200

    except cognito_client.exceptions.NotAuthorizedException:
        return {'status': 'fail', 'message': 'Invalid token or not authorized'}, 401

    except Exception as e:
        LOGGER.error(f"Error fetching current user: {str(e)}")
        return {'status': 'fail', 'message': 'An error occurred while fetching the current user'}, 500




@app.route('/migrate', methods=['POST'])
def migrate():
    try:
        init_db(migrate=True)
        return {"message": "Tablas creadas con éxito"}
    except Exception as e:
        return {"error": str(e)}