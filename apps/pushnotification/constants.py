import os

port = 465  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "noreply.ticketmasterbestseat@gmail.com"
subject = "Message from Ticketmaster Ticket Tracker"
app_password = os.environ.get('MAILER_PW', '')
