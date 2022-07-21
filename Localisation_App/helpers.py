from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_email(email, token):
    subject = 'Your forget password link'
    message = f'Hi, click on this link for reset password http://127.0.0.1:5552/changePassword/{token}/'
    print("message", message)
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True
