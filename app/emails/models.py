from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, engine
from sqlalchemy.orm import relationship
from app.persons.models import Person

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(50), unique=False, index=True)
    message = Column(String(255), unique=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="emails")

class EmailsCotizacion(Base):
    __tablename__ = "emails_cotizacion"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="emails_cotizacion")

Base.metadata.create_all(bind=engine)
