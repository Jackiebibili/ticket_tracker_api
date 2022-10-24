import smtplib, ssl
from email.message import EmailMessage
from constants import *

password = app_password # The password is stored in local

def init_server():
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    return server

def server_login(server, password):
    email = sender_email    
    server.login(email, password)

def server_send_email(server, receiver_email, message):
    receiver_email = receiver_email
    sender_email = sender_email
    subject = "Email from ticketmaster Best Seat App"

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['subject'] = subject

    em.set_content(message)
    server.sendmail(sender_email, receiver_email, em.as_string())

def send_email(receiver_email, message):
    server = init_server()
    server_login(server, password)
    server_send_email(server, receiver_email, message)


send_email(["Frank.Qixiang.Gao@gmail.com"], password)