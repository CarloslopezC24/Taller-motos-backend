import os
import smtplib
from email.message import EmailMessage

def enviar_correo_contacto(nombre, correo_destino, contenido_mensaje):
    msg = EmailMessage()
    msg["Subject"] = "Notificación de Taller Motos"
    msg["From"] = os.getenv("MAIL_USER")
    msg["To"] = correo_destino

    msg.set_content(f"Hola {nombre},\n\n{contenido_mensaje}\n\nSaludos,\nEquipo Taller Motos")

    try:
        with smtplib.SMTP_SSL(os.getenv("MAIL_SERVER"), int(os.getenv("MAIL_PORT", 465))) as smtp:
            smtp.login(os.getenv("MAIL_USER"), os.getenv("MAIL_PASSWORD"))
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error enviando correo: {e}")