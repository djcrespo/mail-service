from pydantic import BaseModel
from app.persons.interfaces import PersonInterface, ContactInterface

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
    objectCotizacion: object
