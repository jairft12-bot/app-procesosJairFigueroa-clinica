import smtplib
from email.mime.text import MIMEText

def enviar_test():
    remitente = "tucorreo@gmail.com"
    contraseña = "tu_contraseña_de_app"
    destinatario = "jairft12@gmail.com"

    msg = MIMEText("Mensaje de prueba", "plain", "utf-8")
    msg["Subject"] = "Prueba envío correo"
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

enviar_test()
