from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import Posting
from .utils import encrypt, decrypt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({'detail': 'Welcome to the home page!'}, status=status.HTTP_200_OK)

### Views for Posting (CRUD)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_posting(request):
    try:
        if request.method == 'POST':
            company = request.user
            title = request.data.get('title')
            department = request.data.get('department')
            city = request.data.get('city')
            country = request.data.get('country')
            soft_skills = request.data.get('soft_skills')
            technical_skills = request.data.get('technical_skills')
            questions = request.data.get('questions')
            recruiter_name = request.data.get('recruiter_name')
            recruiter_email = request.data.get('recruiter_email')
            about_job = request.data.get('about_job')
            about_company = request.data.get('about_company')
            qualification = request.data.get('qualification')
            key_requirements = request.data.get('key_requirements')
            nice_to_have = request.data.get('nice_to_have')
            other_remarks = request.data.get('other_remarks')

            posting = Posting.objects.create(company=company, title=title, department=department, city=city, country=country, soft_skills=soft_skills, technical_skills=technical_skills, questions=questions, recruiter_name=recruiter_name, recruiter_email=recruiter_email, about_job=about_job, about_company=about_company, qualification=qualification, key_requirements=key_requirements, nice_to_have=nice_to_have, other_remarks=other_remarks)

            posting.form_url = f"apply/{encrypt(posting.id)}/"
            posting.save()

            return Response({'message': 'Posting created successfully!', 'status': status.HTTP_201_CREATED})

        return Response({'error': 'Invalid request method', 'status': status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})