from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, engine
from sqlalchemy.orm import relationship


class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), unique=False, index=True)
    message = Column(String(255), unique=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id'), unique=True)
    person = relationship("Person", back_populates="cotizaciones")

Base.metadata.create_all(bind=engine)
