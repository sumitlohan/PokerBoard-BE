from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from poker.celery import app


@app.task
def send_email_task(email, pokerboard, role):
    """
    Celery task for sending invitation email
    """
    template = render_to_string("invite/email_template.html", {"pokerboard": pokerboard}, {"role": role})
    subject = render_to_string("invite/email_subject_template.html", {"pokerboard": pokerboard})
    send_mail(subject=subject, message=template, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
