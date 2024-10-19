import logging
from dataclasses import dataclass

from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import IncidenceRepository

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')


@dataclass
class CreateIncidenceCommand(Command):
    type: str
    title: str
    description: str
    date: int
    user_sub: str


class CreateIncidenceHandler(CommandBaseHandler):
    def handle(self, command: CreateIncidenceCommand):
        LOGGER.info("Handle createIncidentCommand")

        repository = self.incidence_factory.create_object(IncidenceRepository.__class__)
        repository.add(command)


@execute_command.register(CreateIncidenceCommand)
def execute_update_information_command(command:  CreateIncidenceCommand):
    handler = CreateIncidenceHandler()
    handler.handle(command)
