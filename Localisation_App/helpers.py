from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_email(email, token):
    subject = 'Your forget password link'
    message = f'Hi, click on this link for reset password http://test-ubuntu20.pune.cdac.in/changePassword/{token}/'
    print("message", message)
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True
