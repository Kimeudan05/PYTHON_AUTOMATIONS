from dotenv import load_dotenv
import os
import yagmail

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not SENDER_EMAIL or not EMAIL_PASSWORD:
    raise ValueError("Missing email credentials in .env file")

#  initiating connection with SMTP server and Force yagmail to use only given credentials (skip ~/.yagmail lookup)
yag = yagmail.SMTP(user=SENDER_EMAIL, password=EMAIL_PASSWORD, oauth2_file=None)
