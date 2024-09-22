import logging
import json
from dataclasses import dataclass
from pydispatch import dispatcher
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command

LOGGER = logging.getLogger()


@dataclass
class CreateIncidentCommand(Command):
    incidence_type: str
    status: str
    risk_level: str


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateIncidentCommand):
        LOGGER.info("Handle createIncidentCommand")

        event = {
            "status": command.status,
            "risk_level": command.risk_level,
            "incidence_type": command.incidence_type,
        }
        dispatcher.send(signal='CreateIncidentIntegration', event=json.dumps(event))


@execute_command.register(CreateIncidentCommand)
def execute_update_information_command(command:  CreateIncidentCommand):
    handler = UpdateInformationHandler()
    handler.handle(command)
