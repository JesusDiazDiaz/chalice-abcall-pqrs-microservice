from dataclasses import dataclass
from chalicelib.src.seedwork.domain.factory import Factory
from chalicelib.src.seedwork.domain.repository import Repository
from chalicelib.src.modules.domain.repository import UserRepository
from .exceptions import ImplementationNotExistsForFactoryException
from .repository import ClientRepositoryPostgres


@dataclass
class UserFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == UserRepository.__class__:
            return ClientRepositoryPostgres()

        raise ImplementationNotExistsForFactoryException()