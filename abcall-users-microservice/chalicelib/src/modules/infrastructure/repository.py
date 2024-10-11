from uuid import UUID
import logging
from chalicelib.src.modules.domain.repository import UserRepository
from chalicelib.src.modules.infrastructure.dto import User
from chalicelib.src.config.db import db_session
from chalicelib.src.modules.seedwork.infraestructure.utils import handle_db_session


LOGGER = logging.getLogger('abcall-pqrs-microservice')


class UserRepositoryPostgres(UserRepository):
    def __init__(self):
        pass

    def add(self, incidence):
        raise NotImplementedError

    @handle_db_session(db_session)
    def get(self, id):
        incidence = db_session.query(Incidence).filter_by(id=id).first()
        if not incidence:
            raise ValueError("Incidence not found")
        return incidence

    def remove(self, entity):
        raise NotImplementedError

    def get_all(self):
        return db_session.query(Incidence).all()

    def update(self, id, data) -> None:
        raise NotImplementedError
