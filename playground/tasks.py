from time import sleep
from celery import shared_task
from django.http import HttpResponse
from django.core.mail import send_mail, mail_admins, BadHeaderError


@shared_task
def notify_customers(message):
    print("Sending email to customers...")
    print(message)
    sleep(15)
    print("Email sent.")
