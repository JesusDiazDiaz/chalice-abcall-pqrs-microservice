import enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Date, Text
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class DocumentType(enum.Enum):
    cedula = "cedula"
    passport = "passport"
    cedula_extranjeria = "cedula_extranjeria"

class UserRol(enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    agent = "agent"
    regular = "regular"

class CommunicationType(enum.Enum):
    email="email"
    phone="phone"
    sms="sms"
    chat="chat"

class User(Base):
    __tablename__ = 'users'

    cognito_user_sub = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    user_rol = Column(Enum(UserRol), nullable=False)
    client_id = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    communication_type = Column(Enum(CommunicationType), nullable=False)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
