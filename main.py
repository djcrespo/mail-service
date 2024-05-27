import json

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.emails.interfaces import *
from app.persons import models as personsModels
from app.emails import models as emailsModels
from app.cotizaciones import models as cotiModels
from app.emails.services import send_message, send_cotizacion
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
def enviar_cotizacion(correoCotizacion: CorreoCotizacion, db: Session = Depends(get_db)):
    contact = correoCotizacion.contact
    person = correoCotizacion.person
    address = correoCotizacion.address
    object_cotizacion = json.loads(correoCotizacion.objectCotizacion)
    typeOption = object_cotizacion['type']
    object_selectOption = object_cotizacion['selectOption']
    extra_info = object_cotizacion['object']

    if db.query(personsModels.Contact).filter_by(mail=contact.mail).first() is None:
        db_person = personsModels.Person(
            first_name=person.first_name,
            last_name=person.last_name
        )

        db_contact = personsModels.Contact(
            mail=contact.mail,
            phone=contact.phone,
            subject=contact.subject,
            person=db_person
        )
        
        db_address = personsModels.Address(
            street=address.street,
            postal_code=address.postal_code
        )

        db.add(db_person)
        db.add(db_contact)
        db.add(db_address)
        db_person.contact = db_contact
        db_person.address = db_address
        db.commit()
        db.refresh(db_person)
    else:
        db_contact = db.query(personsModels.Contact).filter_by(mail=contact.mail).first()
        db_person = db.query(personsModels.Person).filter_by(id=db_contact.person_id).first()
        db_address = personsModels.Address(
            street=address.street,
            postal_code=address.postal_code
        )
        db.add(db_address)
        db.commit()

    # Guardar cotización
    db_coti = cotiModels.Cotizacion(
        type=object_cotizacion['type']
    )

    db.add(db_coti)
    db.commit()

    # Generar el contenido dinámico para extra_info
    extra_info_html = ''.join([f'<p><strong>{key}:</strong> {value}</p>' for key, value in extra_info.items()])

    template = f"""
                <h2>Información de contacto</h2>
                <p><strong>Nombre:</strong> {person.first_name} {person.last_name} </p>
                <p><strong>Correo electrónico:</strong> {contact.mail}</p>
                <p><strong>Teléfono:</strong> {contact.phone}</p>
                <br>
                <h3>Dirección de envío:</h3>
                <p><strong>Calle:</strong> {address.street}</p>
                <p><strong>Código postal:</strong> {address.postal_code}</p>
                <br>
                <h2>Solicitud de cotización de un {typeOption}:</h2>
                <p><strong>{object_selectOption['producto']} - {object_selectOption['tipo_producto']}</strong></p>
                <p><strong>Condición de adquisición: </strong>{object_selectOption['condiciones_adquisicion']}</p>
                <h3>Información adicional:</h3>
                <p>{extra_info_html}</p>
                """

    send_cotizacion(template)

@app.post('/enviar-mensaje')
def enviar_msj(correoMensaje: CorreoMensaje, db: Session = Depends(get_db)):
    person_data = correoMensaje.person
    contact = correoMensaje.contact
    message = correoMensaje.message

    if db.query(personsModels.Contact).filter_by(mail=contact.mail).first() is None:
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
        db_contact = db.query(personsModels.Contact).filter_by(mail=contact.mail).first()
        db_person = db.query(personsModels.Person).filter_by(id=db_contact.person_id).first()

    # Guardar mensaje
    db_mail = emailsModels.Email(
        subject=contact.subject,
        message=message,
        person=db_person
    )

    db.add(db_mail)
    db.commit()

    # Template del correo
    template = f"""
            <h2>Información de contacto</h2>
            <p><strong>Nombre:</strong> {person_data.first_name} {person_data.last_name}</p>
            <p><strong>Correo electrónico:</strong> {contact.mail}</p>
            <p><strong>Teléfono:</strong> {contact.phone}</p>
            <h2>Mensaje</h2>
            <p>{message}</p>
            """

    send_message(template)
