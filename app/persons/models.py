from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, engine
from sqlalchemy.orm import relationship

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), unique=False, index=True)
    last_name = Column(String(50), unique=False, index=True)
    contact = relationship("Contact", back_populates="person", uselist=False, cascade="all, delete-orphan")
    address = relationship("Address", back_populates="person", uselist=False, cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="person", uselist=False, cascade="all, delete-orphan")
    emails_cotizacion = relationship("EmailsCotizacion", back_populates="person", uselist=False, cascade="all, delete-orphan")
    cotizaciones = relationship("Cotizacion", back_populates="person", uselist=False, cascade="all, delete-orphan")

class Contact(Base):
    __tablename__ = "contact_persons"

    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String(50), unique=True, index=True)
    phone = Column(String(100), unique=False, index=True)
    subject = Column(String(50), unique=False, index=True)
    person_id = Column(Integer, ForeignKey('persons.id'), unique=True)
    person = relationship("Person", back_populates="contact")

class Address(Base):
    __tablename__ = "address_persons"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(50), unique=False, index=True)
    postal_code = Column(String(10), unique=False, index=True)
    person_id = Column(Integer, ForeignKey('persons.id'), unique=True)
    person = relationship("Person", back_populates="address")

Base.metadata.create_all(bind=engine)
