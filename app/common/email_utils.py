import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to_email):
    """
    Sends an email using SMTP with SSL encryption.

    This function sends an email with a specified subject and body to a recipient's email address
    using environment variables for the sender's email and password.

    Args:
        subject (str): The subject line of the email.
        body (str): The body content of the email.
        to_email (str): The recipient's email address.

    Environment Variables:
        FROM_EMAIL (str): The sender's email address.
        PASSWORD (str): The password for the sender's email account.

    Prints:
        A success message if the email is sent successfully.
        An error message if sending fails.

    Exceptions:
        Any exceptions raised during the SMTP connection or email sending process will be caught and printed.
    """
    from_email = os.getenv("FROM_EMAIL")
    from_password = os.getenv("PASSWORD")
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        print('Email sent successfully')
    except Exception as e:
        print(f'Error sending email: {e}')