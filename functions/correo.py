import datetime
import smtplib
from email.mime.text import MIMEText
import random
import hashlib, secrets
import string
from datetime import *
from fastapi import HTTPException
from email.message import EmailMessage

from database import *

char = (string.digits+string.
        ascii_letters+string.punctuation)

""" class Sender:
    Email_sender = ''
    sender_password = ''

    def init(self,Email_sender,sender_password):
        self.Email_sender = Email_sender
        self.sender_password = sender_password

    print(Email_sender, " ", sender_password)

    def Send_M(self, subject, receiver, file, code):#sujeto, el que recibe, el archivo de muestra, codigo de verificacion
        Myfile = open(file, "r", encoding="utf-8")
        readFile = Myfile.read()
        readFile = readFile.replace("CODE", code)
        readFile = readFile.replace("CORREO", receiver)
        msg = MIMEText(readFile, 'html')
        msg['Subject'] = subject
        msg['From'] = self.Email_sender
        msg['To'] = receiver
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as mail:
            mail.login(self.Email_sender, self.sender_password)
            mail.sendmail(self.Email_sender, receiver, msg.as_string()) """

""" async def SendEmail(correo):
    sender = Sender(Email_sender="maria.servidor.vpn@gmail.com",sender_password="jpwp ahhs lyly yikm")
    p1 = ''.join(random.choice(char) for i in range(3))
    p2 = ''.join(random.choice(char) for i in range(3))
    p3 = ''.join(random.choice(char) for i in range(3))
    code = p1+'-'+p2+'-'+p3 #o63-948-eu3
    sender.Send_M(subject="Cambio de Contraseña", receiver=correo, file="html/mensaje.html", code=code)
    h1 = hashlib.sha512(code.encode()).hexdigest()
    t = datetime.utcnow() + timedelta(minutes=3)
    print(t)
    llavesmaestra.create(Key=h1, Expire=t)

    return "Email Send Sucessfully" """

async def SendEmail(correo):
    trabajador = Trabajador.select().where(Trabajador.correo == correo).first()

    if trabajador:
        email_address = "maria.servidor.vpn@gmail.com"
        password = "jpwp ahhs lyly yikm"
        p1 = ''.join(random.choice(char) for i in range(3))
        p2 = ''.join(random.choice(char) for i in range(3))
        p3 = ''.join(random.choice(char) for i in range(3))
        #code = p1+'-'+p2+'-'+p3
        code = "http://localhost:4200/enter-password;correo=" + correo
        Myfile = open('functions/html/mensaje.html', "r", encoding="utf-8")
        readFile = Myfile.read()
        readFile = readFile.replace("CODE", code)
        readFile = readFile.replace("CORREO", correo)
        msg = EmailMessage()
        msg['Subject'] = "Envio Prueba"
        msg['From'] = email_address
        msg['To'] = correo
        msg.set_content(readFile, 'html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as mail:
            mail.login(email_address, password)
            mail.send_message(msg)
    
        h1 = hashlib.sha512(code.encode()).hexdigest()
        t = datetime.utcnow() + timedelta(minutes=3)
        print(t)
        llavesmaestra.create(llave=h1, experacion=t)
#
        return "Email Send Sucessfully"
    else:
        raise HTTPException(status_code=404, detail='Worker not found or incorrect email')

async def Compara(Key):
    tiempo = datetime.utcnow()
    cifrado = hashlib.sha512(Key.encode()).hexdigest()
    mensaje = llavesmaestra.select().where(llavesmaestra.llave == cifrado and tiempo <= llavesmaestra.experacion)
    if mensaje:
        return True
    else:
        raise HTTPException(404, 'El código no coincide o Ya Expiro')