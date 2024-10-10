from uuid import UUID
import logging
from chalicelib.src.modules.domain.repository import IncidenceRepository
from chalicelib.src.modules.infrastructure.dto import Incidence, IncidentType
from chalicelib.src.config.db import db_session


LOGGER = logging.getLogger('abcall-pqrs-events-microservice')


class IncidenceRepositoryPostgres(IncidenceRepository):
    def __init__(self):
        pass

    def add(self, incidence):
        LOGGER.info(f"Repository add incidence: {incidence}")

        incidence = Incidence(
            title=incidence.title,
            type=IncidentType[incidence['type']],
            description=incidence.description,
            date=incidence.date
        )
        db_session.add(incidence)
        db_session.commit()
        return incidence

    def get(self, id: UUID):
        raise NotImplementedError

    def remove(self, entity):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self, id, incid) -> None:
        raise NotImplementedError
