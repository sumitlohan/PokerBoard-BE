from django.core.mail import send_mail
from poker.celery import app

@app.task
def send_email_task(email, first_name):
    message = f"""
    Hello {first_name},
    Thank you for joining poker planner!!

    Our Best,
    JTG and the poker planner team
    """
    send_mail("Welcome to poke planner", message=message, from_email="Rohit", recipient_list=[email])
    
