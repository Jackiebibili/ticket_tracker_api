import smtplib, ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv, find_dotenv
from constants import *

load_dotenv(find_dotenv())

receiver_email = receiver_email
password = app_password # The password is stored in local

message = """\
    Subject: Hi there
    This message is sent from Python to give best seat info."""

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


server = init_server()
server_login(server, password)  
server_send_email(server, receiver_email, message)
