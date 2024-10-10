import logging
from chalice import Chalice, BadRequestError
from chalicelib.src.modules.application.commands.create_incident import CreateIncidentCommand
from chalicelib.src.modules.infrastructure.dto import Base
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.config.db import init_db, engine
from chalicelib.src.seedwork.application.queries import execute_query
from chalicelib.src.modules.application.queries.get_incidents import GetIncidentsQuery


app = Chalice(app_name='abcall-pqrs-microservice')
app.debug = True

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')

init_db()


@app.route('/pqrs')
def index():
    query_result = execute_query(GetIncidentsQuery())
    return query_result.result


@app.route('/pqrs', methods=['POST'])
def incidence_post():
    incidence_as_json = app.current_request.json_body

    LOGGER.info("Receive create incident request")
    required_fields = ["title", "type", "description", "date"]
    for field in required_fields:
        if field not in incidence_as_json:
            raise BadRequestError(f"Missing required field: {field}")

    valid_types = ["petition", "claim"]
    if incidence_as_json["type"] not in valid_types:
        raise BadRequestError(f"Invalid 'type' value. Must be one of {valid_types}")

    command = CreateIncidentCommand(
        title=incidence_as_json["title"],
        type=incidence_as_json["type"],
        description=incidence_as_json["description"],
        date=incidence_as_json["date"]
    )

    execute_command(command)

    return {'status': "ok"}



@app.route('/migrate', methods=['POST'])
def migrate():
    try:
        Base.metadata.create_all(bind=engine)
        return {"message": "Tablas creadas con éxito"}
    except Exception as e:
        return {"error": str(e)}