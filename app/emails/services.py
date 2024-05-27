import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]
to_emails = os.environ["TO_EMAILS"].split(" ")

def send_message(html_body):
    params = {
        "from": "Pagina web <web@jarkol.com>",
        "to": to_emails,
        "subject": "Nuevo mensaje desde la página web",
        "html": html_body,
    }

    resend.Emails.send(params)

def send_cotizacion(html_body):
    params = {
        "from": "Pagina web <web@jarkol.com>",
        "to": to_emails,
        "subject": "Nueva solicitud de cotización",
        "html": html_body,
    }

    resend.Emails.send(params)
