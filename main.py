from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.emails.interfaces import *
from app.persons import models as personsModels
from app.emails import models as emailsModels
from app.emails.services import send_message
from db import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
import resend

app = FastAPI()

resend.api_key = os.environ["RESEND_API_KEY"]

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://example.com",
    # Agrega aquí los dominios que desees permitir
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["ORIGINS"].split(" "),  # Permitir estos orígenes
    allow_credentials=True,  # Permitir el envío de cookies
    allow_methods=["*"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir estos headers
)

# Coneccion con la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

personsModels.Base.metadata.create_all(bind=engine)
emailsModels.Base.metadata.create_all(bind=engine)

@app.post('/enviar-cotizacion')
def enviar_cotizacion(correo: CorreoCotizacion):
    contact = correo.contact
    person = correo.person
    cotizacion = correo.objectCotizacion

    template = """
                <h2>Información de contacto</h2>
                <p><strong>Nombre:</strong> {person.first_name} {person.last_name} </p>
                <p><strong>Correo electrónico:</strong> {contact.mail}</p>
                <p><strong>Teléfono:</strong> {contact.phone}</p>
                <h2>Solicitud de cotización de:</h2>
                <p>{object}</p>
                """

    html_content = template.format(
        person=person,
        object=cotizacion,
        contact=contact
    )

    params = {
        "from": "Jarkol.com - Nueva cotización <cotizaciones@jarkol.com>",
        "to": [contact.mail],
        "subject": contact.subject,
        "html": html_content,
    }

    resend.Emails.send(params)

@app.post('/enviar-mensaje')
def enviar_msj(correoMensaje: CorreoMensaje, db: Session = Depends(get_db)):
    person_data = correoMensaje.person
    contact = correoMensaje.contact
    message = correoMensaje.message

    if db.query(personsModels.Person).filter_by(first_name=person_data.first_name).first() is None:
        db_person = personsModels.Person(
            first_name=person_data.first_name,
            last_name=person_data.last_name
        )

        db_contact = personsModels.Contact(
            mail=contact.mail,
            phone=contact.phone,
            subject=contact.subject,
            person=db_person
        )

        db.add(db_person)
        db.add(db_contact)
        db_person.contact = db_contact
        db.commit()
        db.refresh(db_person)
    else:
        db_person = db.query(personsModels.Person).filter_by(first_name=person_data.first_name).first()

    # Guardar mensaje
    db_mail = emailsModels.Email(
        subject=contact.subject,
        message=message,
        person=db_person
    )

    db.add(db_mail)
    db.commit()

    # Template del correo
    template = """
            <h2>Información de contacto</h2>
            <p><strong>Nombre:</strong> {person.first_name} {person.last_name}</p>
            <p><strong>Correo electrónico:</strong> {contact.mail}</p>
            <p><strong>Teléfono:</strong> {contact.phone}</p>
            <h2>Mensaje</h2>
            <p>{message}</p>
            """

    html_content = template.format(
        person=person_data,
        contact=contact,
        message=message
    )

    send_message(html_content)
