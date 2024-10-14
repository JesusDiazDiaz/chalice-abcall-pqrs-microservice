from operator import and_
from uuid import UUID
import logging
from chalicelib.src.modules.domain.repository import UserRepository
from chalicelib.src.modules.infrastructure.dto import User, DocumentType, UserRol, CommunicationType
from chalicelib.src.config.db import db_session
from chalicelib.src.modules.seedwork.infraestructure.utils import handle_db_session


LOGGER = logging.getLogger('abcall-pqrs-microservice')


class UserRepositoryPostgres(UserRepository):
    def __init__(self):
        pass

    def add(self, user):
        LOGGER.info(f"Repository add user: {user}")

        new_user = User(
            cognito_user_sub=user.cognito_user_sub,
            document_type=DocumentType[user.document_type],
            user_rol=UserRol[user.user_rol],
            client_id=user.client_id,
            id_number=user.id_number,
            name=user.name,
            last_name=user.last_name,
            communication_type=CommunicationType[user.communication_type]
        )
        db_session.add(new_user)
        db_session.commit()
        return new_user

    @handle_db_session(db_session)
    def get(self, user_sub):
        user = db_session.query(User).filter_by(user_sub=user_sub).first()
        if not user:
            raise ValueError("user not found")
        return user

    def remove(self, user_sub):
        LOGGER.info(f"Repository remove user: {user_sub}")
        entity = db_session.query(User).filter_by(user_sub=user_sub).first()
        db_session.delete(entity)
        db_session.commit()
        LOGGER.info(f"User {user_sub} removed successfully")

    def get_all(self, query:dict[str, str]):
        if not query:
            return db_session.query(User).all()

        filters = []
        if 'client_id' in query:
            filters.append(User.client_id == query['client_id'])
        if 'name' in query:
            filters.append(User.name.ilike(f"%{query['name']}%"))  # Para una búsqueda parcial (case-insensitive)
        if 'last_name' in query:
            filters.append(User.last_name.ilike(f"%{query['last_name']}%"))
        if 'document_type' in query:
            filters.append(User.document_type == query['document_type'])
        if 'id_number' in query:
            filters.append(User.id_number == query['id_number'])

        return db_session.query(User).filter(and_(*filters)).all()


    def update(self, user_sub, data) -> None:
        LOGGER.info(f"Repository update user sub: {user_sub} with data: {data}")

        user = db_session.query(User).filter_by(cognito_user_sub=user_sub).first()
        if not user:
            raise ValueError("User not found")

        if 'name' in data:
            user.name = data['name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'cellphone' in data:
            user.cellphone = data['cellphone']
        if 'client_id' in data:
            user.client_id = data['client_id']
        if 'document_type' in data:
            user.document_type = DocumentType[data['document_type']]
        if 'user_rol' in data:
            user.user_rol = UserRol[data['user_rol']]
        if 'communication_type' in data:
            user.communication_type = CommunicationType[data['communication_type']]

        db_session.commit()
        LOGGER.info(f"User {user_sub} updated successfully")
