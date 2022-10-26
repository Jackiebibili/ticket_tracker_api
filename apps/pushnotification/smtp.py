from smtplib import SMTP_SSL
from ssl import create_default_context
from email.message import EmailMessage
from . import constants


def init_server():
    context = create_default_context()
    server = SMTP_SSL(constants.smtp_server, constants.port, context=context)
    return server


def server_login(server: SMTP_SSL, password: str):
    return server.login(constants.sender_email, password)


def server_send_email(server: SMTP_SSL, receiver_emails: list[str], message: str):
    em = EmailMessage()
    em['From'] = constants.sender_email
    em['To'] = receiver_emails
    em['subject'] = constants.subject

    em.set_content(message)
    return server.sendmail(constants.sender_email, receiver_emails, em.as_string())


def send_email(receiver_emails: list[str], messages: list[str]):
    if len(messages) == 0:
        return
    # print(messages[0])
    try:
        err = server_send_email(server, receiver_emails, messages[0])
        if err is not None:
            raise Exception('could not send email to the receiver')
    except Exception as ex:
        print(ex)


server = init_server()


def auth_server():
    global server
    server_login(server, constants.app_password)
