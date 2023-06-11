import streamlit
from dotenv import load_dotenv
import os
import ssl
from email.message import EmailMessage
import smtplib
import streamlit as st
import re

class Gmail:

    def __init__(self):
        load_dotenv(dotenv_path="config/cred.env")
        self.sender = os.environ.get("GMAIL")

        if self.sender.endswith('"') or self.sender.endswith("'"):
            self.sender = self.sender[:-1]
        self.password = os.environ.get("GMAIL_PASSWORD")

    def send(self, name_file, content, receiver):

        email_sender = self.sender
        email_password = self.password
        email_receiver = receiver

        subject = f"{name_file}'s audio transcription"

        body = f"""
        {content}
        """

        em = EmailMessage()

        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    @staticmethod
    def check (mail):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat, mail):
            return True
        return False
