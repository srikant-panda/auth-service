from os import getenv
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = str(getenv("SMTP_USER"))
SMTP_PASSWORD = str(getenv("SMTP_PASSWORD"))
SMTP_PORT = getenv("SMTP_PORT")
SMTP_HOST  = str(getenv("SMTP_HOST"))

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
        )