# utils.py

from django.core.mail import send_mail
from django.conf import settings
import random


def send_otp_via_email(email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    subject = "RecruitEase - OTP for Password Reset"
    message = f"Your OTP for password reset is {otp}. Please do not share this OTP"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)
    #  Verifty response of send_mail
    return otp
