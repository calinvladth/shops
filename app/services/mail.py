import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to, subject, body):
    try:
        message = Mail(
            from_email=os.environ.get("MAIL"),
            to_emails=to,
            subject=subject,
            html_content=body,
        )
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        return sg.send(message)
    except Exception as e:
        return False
