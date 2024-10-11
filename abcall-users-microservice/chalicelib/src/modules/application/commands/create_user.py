import logging
import json
from dataclasses import dataclass
from pydispatch import dispatcher
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')


@dataclass
class CreateUserCommand(Command):
    cognito_user_sub: str
    document_type: str
    client_id: str
    id_number: str
    name: str
    last_name: str


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateUserCommand):
        LOGGER.info("Handle createIncidentCommand")

        event = {
            "type": command.type,
            "title": command.title,
            "description": command.description,
            "date": command.date
        }
        dispatcher.send(signal='CreateIncidentIntegration', event=json.dumps(event))


@execute_command.register(CreateUserCommand)
def execute_update_information_command(command:  CreateUserCommand):
    handler = UpdateInformationHandler()
    handler.handle(command)
