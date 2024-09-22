from uuid import UUID
import logging
from chalicelib.src.modules.domain.repository import IncidenceRepository

LOGGER = logging.getLogger('abcall-pqrs-events-microservice')


class IncidenceRepositoryPostgres(IncidenceRepository):
    def __init__(self):
        pass

    def add(self, incidence):
        LOGGER.info(f"Repository add incidence: {incidence}")

        return incidence

    def get(self, id: UUID):
        raise NotImplementedError

    def remove(self, entity):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self, id, incid) -> None:
        raise NotImplementedError


    # def update(self, id, incidence) -> None:
    #     LOGGER.info(f"update property: {property}")
    #
    #     property_dto = db.session.query(PropertyDto).get(id)
    #
    #     LOGGER.info(f"update property_dto: {property.id}, {property_dto.construction_type}")
    #
    #     property_dto.size_sqft = property.characteristics.size_sqft
    #     property_dto.construction_type = property.characteristics.construction_type
    #     property_dto.floors = property.characteristics.floors
    #
    #     db.session.add(property_dto)

        # db.session.commit()

        # return self.property_factory.create_object(property_dto, PropertyMapper())
