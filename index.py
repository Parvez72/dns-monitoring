import socket
from time import sleep
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from os import environ

SEND_GRID_KEY = environ.get('SENDGRID_API_KEY')
RECEIVERS = environ.get('RECEIVERS')
TO_EMAILS = []

if SEND_GRID_KEY is None:
    print("[ERROR] SendGrid key not provided please provide SENDGRID_API_KEY=key in environment variables, "
          "stopping the service")
    exit(1)

if RECEIVERS is None:
    print("[ERROR] Receivers not provided, please give environment variable RECEIVERS=ex@gd.com,ex@ds.com")
    exit(1)
else:
    for i in RECEIVERS.split(","):
        TO_EMAILS.append(i.strip())

print('[INFO] Sending mails to ', TO_EMAILS)


def send_mail(message):
    message = Mail(
        from_email='infra@yellowmessenger.com',
        to_emails=TO_EMAILS,
        subject='Failed to dns resolve',
        html_content='<p>' + message + '</p>')
    try:
        sg = SendGridAPIClient(SEND_GRID_KEY)
        response = sg.send(message)
        print("[INFO] Email Sent", response.status_code)
    except Exception as ex:
        print("[ERROR] Failed to send mail", ex)


while True:
    try:
        localAddress = socket.gethostbyname("data-service.services")
        print("[INFO] Found local address", localAddress)
    except Exception as e:
        send_mail("Failed to resolve local address for data-service.services " + str(e))
        print("[ERROR] Local address not found for data-service.services", e)
    try:
        localAddress = socket.gethostbyname("google.co.in")
        print("[INFO] Found public address for google.co.in", localAddress)
    except Exception as e:
        send_mail("Failed to resolve public address for google.co.in " + str(e))
        print("[ERROR] Public address not found for google.co.in", e)
    sleep(2)

