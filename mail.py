import os
import  smtplib
from email.mime.text import MIMEText
from logger import logger
from dotenv import load_dotenv


# loading .env Variables
load_dotenv()
user = os.getenv('USER')
mailPassword= os.getenv('PASSWORD')

# Function for Send Mail
def mailSend(message:str,subject:str,recipient:str):
    subject = subject
    body = message
    sender = user
    recipients = recipient
    password = mailPassword
    msg = MIMEText(body)
    msg['Subject']= subject
    msg['From']= sender
    msg['To']= ','.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtpServer:
        smtpServer.login(sender, password)
        smtpServer.sendmail(sender, recipients, msg.as_string())
    logger.info("Message Sent")