from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from poker.celery import app

@app.task
def send_email_task(email, first_name):
    template = render_to_string("user/email_template.html", {"first_name": first_name})
    subject = "Welcome to poke planner"
    send_mail(subject=subject, message=template, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
    
