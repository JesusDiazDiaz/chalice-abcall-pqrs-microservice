import logging
from chalice import Chalice
from chalicelib.src.modules.application.commands.create_incident import CreateIncidentCommand
from chalicelib.src.seedwork.application.commands import execute_command

app = Chalice(app_name='abcall-pqrs-microservice')
app.debug = True

LOGGER = logging.getLogger()


@app.route('/pqrs', methods=['POST'])
def incidence_post():
    incidence_as_json = app.current_request.json_body

    LOGGER.info("Receive create incident request")

    command = CreateIncidentCommand(
        incidence_type=incidence_as_json["incidence_type"],
        status=incidence_as_json["status"],
        risk_level=incidence_as_json["risk_level"],
    )

    execute_command(command)

    return {'status': "ok"}