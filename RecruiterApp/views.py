from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Posting
from .serializers import CompanySerializer
from .utils import get_company, encrypt, decrypt
# Testing ...
@api_view(['POST'])
def register_view(request):
    try:
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Company registered successfully', 'status': status.HTTP_201_CREATED})
        
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

@api_view(['POST'])
def logout_view(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)

        company = response
        company.refresh_token = None
        company.save()
        return Response({'message': 'Logged out successfully', 'status': status.HTTP_200_OK})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
    

# This is just for testing purposes
@api_view(['GET'])
def home_view(request):
    response, isAuthenticated = get_company(request)

    if not isAuthenticated:
        return Response(response)
    
    company = response
    return Response({'data': {'company_name': company.name}, 'status': status.HTTP_200_OK})


### Views for Posting (CRUD)

# View for creating a new posting
@api_view(['POST'])
def create_posting(request):
    try:
        if request.method == 'POST':
            response, isAuthenticated = get_company(request)
            if not isAuthenticated:
                return Response(response)
            
            company = response
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
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

@api_view(['GET'])
def get_postings(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)
        
        company = response
        id = request.GET.get('id')
        if id:
            postings = Posting.objects.filter(id=decrypt(id))
        else:
            postings = Posting.objects.filter(company=company)

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
def update_posting(request):
    try:
        if request.method == 'PUT':
            response, isAuthenticated = get_company(request)

            if not isAuthenticated:
                return Response(response)
            
            company = response
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
def delete_posting(request):
    try:
        if request.method == 'DELETE':
            response, isAuthenticated = get_company(request)

            if not isAuthenticated:
                return Response(response)
            
            company = response
            posting_id = decrypt(request.data.get('id'))
            posting = Posting.objects.get(id=posting_id)
            if not posting:
                return Response({'error': 'Posting Not Found', 'status': status.HTTP_404_NOT_FOUND})
            
            posting.delete()
            return Response({'message': 'Posting deleted successfully', 'status': status.HTTP_200_OK})

    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

