from RecruiterApp.models import Company, Tokens
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
        token = request.headers.get("Authorization")

        if not token:
            return (
                {
                    "error": "Authorization token not provided",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                False,
            )

        try:
            token_entry = Tokens.objects.get(token=token, is_valid=True)
            email = token_entry.email
            print(email)
            try:
                company = Company.objects.get(email=email)
                return (company, True)
            except Company.DoesNotExist:
                return (
                    {"error": "Invalid Token", "status": status.HTTP_400_BAD_REQUEST},
                    False,
                )
        except Company.DoesNotExist:
            return (
                {"error": "Invalid Token", "status": status.HTTP_400_BAD_REQUEST},
                False,
            )
    except Exception as e:
        print(e)
        return (
            {
                "error": "Internal Server Error",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            False,
        )


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
        html_message=message,  # Add HTML content support
    )
    return True

from django.template.loader import render_to_string

def send_status_update_email(candidate, new_status, context):
    templates = {
        'Application Submitted': 'emails/application_submitted.html',
        'Under Review': 'emails/under_review.html',
        'Interview Scheduled': 'emails/interview_notification.html',
        'Under Evaluation': 'emails/under_evaluation.html',
        'Offer Sent': 'emails/offer_sent.html',
        'Not Selected': 'emails/not_selected.html',
    }

    template_name = templates.get(new_status)
    print(template_name)
    if not template_name:
        return False, {'error': 'Invalid application status provided', 'status': status.HTTP_400_BAD_REQUEST}

    email_content = render_to_string(template_name, context)
    print("sending email")
    print(candidate.candidate.email)
    email_sent = send_email_update(
        to=candidate.candidate.email,
        subject=f"Application Status Update: {new_status}",
        message=email_content
    )  
    print(email_sent)

    if not email_sent:
        return False, {'error': 'Failed to send email', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}

    return True, {'message': 'Candidate status updated successfully and email sent', 'status': status.HTTP_200_OK}

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import io
import base64

def b64_to_pdf(b64content):
    try:
        buffer = io.BytesIO()
        content = base64.b64decode(b64content)
        buffer.write(content)
        buffer.seek(0)  # Move the cursor to the beginning of the buffer
        return buffer
    except (TypeError, base64.binascii.Error) as e:
        print(f"Error decoding base64 content: {e}")
        return None

def send_email_with_pdf(to_email, b64content, context, subject):
    # Generate the PDF content as a BytesIO object
    pdf_buffer = b64_to_pdf(b64content)

    if pdf_buffer is None:
        return False, {'message': 'Failed to decode PDF content', 'status': '400 Bad Request'}

    # Render the email content
    template_name = 'emails/offer_sent.html'
    email_content = render_to_string(template_name, context)
    
    # Create the email
    email = EmailMessage(
        subject=subject,
        body=email_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )

    # Attach the PDF
    try:
        pdf_data = pdf_buffer.read()
        email.attach('Offer Letter.pdf', pdf_data, 'application/pdf')
    except Exception as e:
        print(f"Error attaching PDF: {e}")
        return False, {'message': 'Failed to attach PDF', 'status': '500 Internal Server Error'}
    finally:
        pdf_buffer.close()

    # Send the email
    try:
        email.send()
        return True, {'message': 'Offer letter sent successfully', 'status': '200 OK'}
    except Exception as e:
        print(f"Error sending email: {e}")
        return False, {'message': 'Failed to send email', 'status': '500 Internal Server Error'}
