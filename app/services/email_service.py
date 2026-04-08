import aiosmtplib
from email.message import EmailMessage

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = "srikantcyber09@gmail.com"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username="srikantcyber09@gmail.com",
            password="pjxw xoca ppge tqui",
        )