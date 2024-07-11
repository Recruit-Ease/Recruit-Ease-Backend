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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_postings(request):
    try:
        id = request.GET.get('id')
        if id:
            postings = Posting.objects.filter(id=decrypt(id))
        else:
            postings = Posting.objects.filter(company=request.user)

        data = []
        for posting in postings:
            data.append({
                'id': encrypt(posting.id),
                'title': posting.title,
                'department': posting.department,
                'city': posting.city,
                'country': posting.country,
                'posting_date': posting.posting_date,
                'expiration_date': posting.expiration_date,
                'soft_skills': posting.soft_skills,
                'technical_skills': posting.technical_skills,
                'questions': posting.questions,
                'recruiter_name': posting.recruiter_name,
                'recruiter_email': posting.recruiter_email,
                'about_job': posting.about_job,
                'about_company': posting.about_company,
                'qualification': posting.qualification,
                'key_requirements': posting.key_requirements,
                'nice_to_have': posting.nice_to_have,
                'other_remarks': posting.other_remarks,
                'is_active': posting.is_active,
                'form_url': posting.form_url
            })

        return Response({'data': data, 'message': 'Postings Received Successfully', 'status': status.HTTP_200_OK})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_posting(request):
    try:
        if request.method == 'PUT':
            posting_id = decrypt(request.data.get('id'))
            posting = Posting.objects.get(id=posting_id)
            if not posting:
                return Response({'error': 'Posting not found', 'status': status.HTTP_404_NOT_FOUND})
            
            for field, value in request.data.items():
                if field != "id" and hasattr(posting, field):
                    setattr(posting, field, value)
            posting.save()

            return Response({'message': 'Posting updated successfully', 'status': status.HTTP_200_OK})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_posting(request):
    try:
        if request.method == 'DELETE':
            posting_id = decrypt(request.data.get('id'))
            posting = Posting.objects.get(id=posting_id)
            if not posting:
                return Response({'error': 'Posting Not Found', 'status': status.HTTP_404_NOT_FOUND})
            
            posting.delete()
            return Response({'message': 'Posting deleted successfully', 'status': status.HTTP_200_OK})

    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

# Views for Candidate Form (CRUD)

# View to get a Posting Details to Create Form
@api_view(['GET'])
@permission_classes([AllowAny])
def get_posting_details(request, id):
    try:
        posting_id = decrypt(id)
        posting = Posting.objects.get(id=posting_id, is_active=True)

        if not posting:
            return Response({'error': 'Posting not found', 'status': status.HTTP_404_NOT_FOUND})
        
        data = {
            'id': encrypt(posting.id),
            'title': posting.title,
            'department': posting.department,
            'city': posting.city,
            'country': posting.country,
            'posting_date': posting.posting_date,
            'expiration_date': posting.expiration_date,
            'soft_skills': posting.soft_skills,
            'technical_skills': posting.technical_skills,
            'questions': posting.questions,
            'recruiter_name': posting.recruiter_name,
            'recruiter_email': posting.recruiter_email,
            'about_job': posting.about_job,
            'about_company': posting.about_company,
            'qualification': posting.qualification,
            'key_requirements': posting.key_requirements,
            'nice_to_have': posting.nice_to_have,
            'other_remarks': posting.other_remarks,
            'is_active': posting.is_active,
            'form_url': posting.form_url
        }

        return Response({'data': data, 'message': 'Posting Data Received Sucessfully', 'status': status.HTTP_200_OK})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})