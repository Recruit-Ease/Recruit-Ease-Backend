from RecruiterApp.models import Company
from rest_framework import status
from django.core import signing

def encrypt(data):
    # Serialize and sign the data
    signed_data = signing.dumps(data)
    return signed_data

def decrypt(signed_data):
    try:
        # Verify and deserialize the signed data
        data = signing.loads(signed_data)
        return data
    except signing.BadSignature:
        # Handle invalid or tampered data
        return None

def get_company(request):
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return ({'error': 'Authorization token not provided', 'status':status.HTTP_400_BAD_REQUEST}, False)
        
        try:
            company = Company.objects.get(refresh_token=token)
            return (company, True)
        except Company.DoesNotExist:
            return ({'error': 'Invalid Token', 'status': status.HTTP_400_BAD_REQUEST}, False)
    except Exception as e:
        return ({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, False)
    


from django.core.mail import send_mail
from django.conf import settings

def send_email_update(to, subject, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to]

    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False,
        html_message=message  # Add HTML content support
    )
    return True