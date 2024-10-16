from uuid import UUID
import logging
from chalicelib.src.modules.domain.repository import IncidenceRepository
from chalicelib.src.modules.infrastructure.dto import Incidence
from chalicelib.src.config.db import db_session, init_db
from chalicelib.src.seedwork.infrastructure.utils import handle_db_session
LOGGER = logging.getLogger('abcall-pqrs-microservice')


class IncidenceRepositoryPostgres(IncidenceRepository):
    def __init__(self):
        self.db_session = init_db()

    def add(self, incidence):
        raise NotImplementedError

    @handle_db_session(db_session)
    def get(self, id):
        incidence = self.db_session.query(Incidence).filter_by(id=id).first()
        if not incidence:
            raise ValueError("Incidence not found")
        return incidence

    def remove(self, entity):
        raise NotImplementedError

    def get_all(self):
        return self.db_session.query(Incidence).all()

    def update(self, id, data) -> None:
        raise NotImplementedError
