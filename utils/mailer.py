import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

sender_password = os.getenv("SENDER_PASSWORD")
sender_email = os.getenv("SEND_EMAIL")  

def send_email(to_email: str, subject: str, content: str):
    if not sender_email or not sender_password:
        raise ValueError("Sender email or password not set in environment variables.")
    
    yag = yagmail.SMTP(user=sender_email, password=sender_password)
    yag.send(
        to=to_email,
        subject=subject,
        contents=content
    )
    print(f"✅ Email sent to {to_email}")
