import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time
from utils.config import SMTP_USER, SMTP_PASSWORD

def send_email(to: str, subject: str, plain_text: str, html_content: str) -> bool:
    '''Send an email with both plain text and HTML content.'''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to

    # Attach plain text and HTML content
    msg.attach(MIMEText(plain_text, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    # Retry once after 5 minutes if the first attempt fails
    for attempt in range(2):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, to, msg.as_string())
            return True
        except smtplib.SMTPException as e:
            if attempt == 0:
                time.sleep(300)  # Wait 5 minutes before retrying
            else:
                raise e
    return False

def send_daily_digest(to: str) -> bool:
    '''Send the daily digest email.'''
    subject = f'Magic Formula Daily Digest – {datetime.now().strftime('%Y-%m-%d')}'
    plain_text, html_content = generate_email_content()
    return send_email(to, subject, plain_text, html_content)
