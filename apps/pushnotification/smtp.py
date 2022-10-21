import smtplib, ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv, find_dotenv

port = 465  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "noreply.ticketmasterbestseat@gmail.com"
subject = "Message from Ticketmaster Ticket-Tracker"



def send_email(to_email, message):

    load_dotenv(find_dotenv())

    receiver_email = to_email
    password = "?????????" # The password is stored in local

    message = """\
    Subject: Hi there
    This message is sent from Python to give best seat info."""

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['subject'] = subject

    em.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, em.as_string())

