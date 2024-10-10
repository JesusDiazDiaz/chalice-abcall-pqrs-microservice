import json
import logging
from chalice import Chalice
from chalicelib.src.modules.application.commands.create_incident import CreateIncidenceCommand
from chalicelib.src.seedwork.application.commands import execute_command

app = Chalice(app_name='abcall-pqrs-events-microservice')
# Enable DEBUG logs.
app.log.setLevel(logging.DEBUG)

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')

@app.on_sns_message(topic='AbcallPqrsTopic')
def handle_sns_message(event):
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

    incidence_as_json = json.loads(event.message)

    command = CreateIncidenceCommand(
        incidence_type=incidence_as_json["incidence_type"],
        status=incidence_as_json["status"],
        risk_level=incidence_as_json["risk_level"],
    )

    execute_command(command)