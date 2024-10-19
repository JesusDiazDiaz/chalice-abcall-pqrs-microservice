from datetime import datetime, timedelta
from uuid import UUID
import logging
from sqlalchemy.exc import SQLAlchemyError
from chalicelib.src.modules.domain.repository import IncidenceRepository
from chalicelib.src.modules.infrastructure.dto import Incidence, IncidentType, Status, CommunicationType
from chalicelib.src.config.db import db_session, init_db
from chalicelib.src.modules.infrastructure.facades import MicroservicesFacade

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')


class IncidenceRepositoryPostgres(IncidenceRepository):
    def __init__(self):
        self.db_session = init_db()

    def _close_session(self):
        self.db_session.close()

    def add(self, incidence):
        LOGGER.info(f"Repository add incidence: {incidence}")

        incidence_date = datetime.fromtimestamp(incidence.date)
        estimated_close_date = incidence_date + timedelta(days=8)

        LOGGER.info(f"Get user by sub {incidence.user_sub}")
        # TODO: Add retrieve user
        # facade = MicroservicesFacade()
        # current_user = facade.get_user(incidence.user_sub)

        try:
            incidence = Incidence(
                client_id='1',
                subject=incidence.title,
                description=incidence.description,
                status=Status.ABIERTO,
                date=incidence_date,
                estimated_close_date=estimated_close_date,
                user_id='1',
                type=IncidentType.PETICION,
                type_communication=CommunicationType.EMAIL
            )

            self.db_session.add(incidence)
            self.db_session.commit()

            return incidence
        except SQLAlchemyError as e:
            LOGGER.error(f"Error adding incidence: {e}")
            self.db_session.rollback()
        finally:
            self._close_session()

    def get(self, id: UUID):
        raise NotImplementedError

    def remove(self, entity):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self, id, incid) -> None:
        raise NotImplementedError
