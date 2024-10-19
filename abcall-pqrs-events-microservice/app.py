import json
import logging
from chalice import Chalice
from chalicelib.src.modules.application.commands.create_incident import CreateIncidenceCommand
from chalicelib.src.seedwork.application.commands import execute_command

app = Chalice(app_name='abcall-pqrs-events-microservice')
app.log.setLevel(logging.DEBUG)

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')


@app.on_sns_message(topic='AbcallPqrsTopic')
def handle_sns_message(event):
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

    incidence_as_json = json.loads(event.message)

    command = CreateIncidenceCommand(
        title=incidence_as_json["title"],
        type=incidence_as_json["type"],
        description=incidence_as_json["description"],
        date=incidence_as_json["date"],
        user_sub=incidence_as_json["user_sub"]
    )

    execute_command(command)