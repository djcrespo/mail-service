from pydantic import BaseModel

class PersonInterface(BaseModel):
    first_name: str
    last_name: str

class ContactInterface(BaseModel):
    mail: str
    phone: str
    subject: str

class AddressInterface(BaseModel):
    street: str
    postal_code: int
