from pydantic import BaseModel
from app.persons.interfaces import PersonInterface, ContactInterface, AddressInterface
from typing import Any

class CorreoMensaje(BaseModel):
    person: PersonInterface
    contact: ContactInterface
    message: str

class Mensaje(BaseModel):
    subject: str
    messaje: str

class CorreoCotizacion(BaseModel):
    person: PersonInterface
    contact: ContactInterface
    address: AddressInterface
    objectCotizacion: str
