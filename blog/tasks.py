import bs4
import django
import requests

from blog.models import MyUser, UserPost
from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings

django.setup()


@shared_task
def send_email(subject, message, from_email):
    send_mail(subject, message, settings.NOREPLY_EMAIL, [from_email])

# @shared_task
# def send_email_to_user(subject, message, from_email):
#     send_mail(subject, message, settings.NOREPLY_EMAIL, [from_email],
#               html_message=f"<p>You have new comment: {''}</p>")
#
#


@shared_task
def send_email_to_admin(subject, message, from_email):
    send_mail(subject, message, settings.NOREPLY_EMAIL, [from_email])


@shared_task
def contact_email(subject, message, email):
    send_mail(subject, message, settings.NOREPLY_EMAIL, email)
