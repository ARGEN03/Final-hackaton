from .send_mail import send_confirmation_email, send_password_reset_email
from config.celery import app

@app.task()
def send_confirmation_email_task(email, code):
    send_confirmation_email(email, code)

@app.task()
def send_password_reset_email_task(email, reset_link):
    send_password_reset_email(email, reset_link)
