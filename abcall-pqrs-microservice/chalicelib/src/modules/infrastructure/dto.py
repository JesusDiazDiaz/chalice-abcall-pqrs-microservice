import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Date, Text


Base = declarative_base()


class IncidentType(enum.Enum):
    petition = "petition"
    claim = "claim"


class Incidence(Base):
    __tablename__ = 'incidences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(Enum(IncidentType), nullable=False)
    description = Column(Text, nullable=False)
