from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import resend

app = FastAPI()

resend.api_key = os.environ["RESEND_API_KEY"]

# Modelo Pydantic para datos de correo
class Correo(BaseModel):
    destinatario: str
    asunto: str
    mensaje: str

class CorreoMensaje(BaseModel):
    name: str
    email: str
    phone: str
    subject: str
    message: str

class CorreoCotizacion(BaseModel):
    person: object
    objectCotizacion: object

@app.post('/enviar-cotizacion')
def enviar_cotizacion(correo: CorreoCotizacion):
    template = """
                <h2>Información de contacto</h2>
                <p><strong>Nombre:</strong> {person.name}</p>
                <p><strong>Correo electrónico:</strong> {person.mail}</p>
                <p><strong>Teléfono:</strong> {person.phone}</p>
                <h2>Cotización por el producto:</h2>
                <p>{message}</p>
                """

    html_content = template.format(
        person=correo.person,
        object=correo.object
    )

    params = {
        "from": "Jarkol.com - Nueva cotización <cotizaciones@jarkol.com>",
        "to": [correo.destinatario],
        "subject": correo.asunto,
        "html": correo.mensaje,
    }

    resend.Emails.send(params)

@app.post('/enviar-mensaje')
def enviar_msj(correoMensaje: CorreoMensaje):
    # Template del correo
    template = """
            <h2>Información de contacto</h2>
            <p><strong>Nombre:</strong> {name}</p>
            <p><strong>Correo electrónico:</strong> {email}</p>
            <p><strong>Teléfono:</strong> {phone}</p>
            <h2>Mensaje</h2>
            <p>{message}</p>
            """

    html_content = template.format(
        name=correoMensaje.name,
        email=correoMensaje.email,
        phone=correoMensaje.phone,
        message=correoMensaje.message
    )

    params = {
        "from": "Jarkol.com - Nuevo mensaje <cotizaciones@jarkol.com>",
        "to": ["dj.crespo.castilla@gmail.com", "didier.1998.boris@gmail.com"],
        "subject": correoMensaje.subject,
        "html": html_content,
    }

    resend.Emails.send(params)
