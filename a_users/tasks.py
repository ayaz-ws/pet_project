from django.urls import reverse
from django.core.mail import send_mail
from decouple import config
from .models import Profile
from a_core.celery import app


@app.task
def send_verification_email(profile_uuid, verify_url):
    profile = Profile.objects.get(verify_uuid=profile_uuid)
    subject = 'Подтверждение email на сайте "Django Pet Project"'
    message = f'Здравствуйте, для подтверждения своего прфоиля вам необходимо перейти по ссылке {verify_url}'
    from_email = config("EMAIL_HOST_USER")
    recipient_list = [profile.user.email]
    send_mail(subject, message, from_email, recipient_list)