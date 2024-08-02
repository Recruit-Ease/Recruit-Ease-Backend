from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CompanyProfile, Posting, Application, Company
from .serializers import CompanySerializer
from .utils import get_company, encrypt, decrypt
from CandidateApp.models import Candidate, CandidateProfile
from .utils import send_email_update
from django.template.loader import render_to_string
from .utils import send_status_update_email

@api_view(['POST'])
def register_view(request):
    try:
        email = request.data.get('email')
        if Company.objects.filter(email=email.lower()).exists() or Candidate.objects.filter(email=email.lower()).exists():
            return Response({'error': 'User with this email already exists ---', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
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

            return Response({'message': 'Posting created successfully!',
                             'posting_link':posting.form_url,
                             'status': status.HTTP_201_CREATED})

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
            applications = Application.objects.filter(posting=posting)
            num_applications = applications.count()
            data.append({
                'id': encrypt(posting.id),
                'title': posting.title,
                'department': posting.department,
                'city': posting.city,
                'country': posting.country,
                'posting_date': posting.posting_date,
                'deadline': posting.expiration_date,
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
                'posting_link': posting.form_url,
                'num_applications': num_applications
            })

        if id:
            data = data[0]

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

# # Views for Candidate Form (CRUD)

# View to get a Posting Details to Create Form
@api_view(['GET'])
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
            'deadline': posting.expiration_date,
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
            'posting_link': posting.form_url
        }

        return Response({'data': data, 'message': 'Posting Data Received Sucessfully', 'status': status.HTTP_200_OK})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

# View to get the candidate data for a posting
@api_view(['GET'])
def get_application(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)
        
        company = response
        
        application_id = request.GET.get('application_id')
        
        posting_id = request.GET.get('posting_id')
        if application_id:
            application = Application.objects.filter(id=decrypt(application_id))
        elif posting_id:
            application = Application.objects.filter(posting_id=decrypt(posting_id))
        else:
            application = Application.objects.filter(posting__company=company)

        data = []
        for app in application:
            candidateProfile = CandidateProfile.objects.get(candidate=app.candidate)
            data.append({
                'application_id': encrypt(app.id),
                'posting_id': encrypt(app.posting.id),
                'company_name': app.posting.company.name,
                'job_title': app.posting.title,
                'location': app.posting.company.address,
                'first_name': candidateProfile.first_name,
                'last_name': candidateProfile.last_name,
                'email': app.candidate.email,
                'phone': candidateProfile.phone,
                'address': candidateProfile.address,
                'city': candidateProfile.city,
                'province': candidateProfile.province,
                'country': candidateProfile.country,
                'postal_code': candidateProfile.postal_code,
                'resume': app.resume,
                'legal_questions': app.legal_questions,
                'questions': app.questions,
                'created_at': app.created_at,
                'status': app.status
            })
        
        if application_id:
            data = data[0]
        
        return Response({'data': data, 'message': 'Applications Received successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_application(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)
        
        company = response
        if request.method == 'DELETE':
            application_id = request.data.get('application_id')

            application_id = decrypt(application_id)
            application = Application.objects.filter(id=application_id)
            if not application.exists():
                return Response({'error': 'Application not found', 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
            application.delete()

            return Response({'message': 'Application deleted successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def send_email_candidate(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)

        company = response
        candidate_id = decrypt(request.data.get('id'))
        candidate = Application.objects.filter(id=candidate_id).first()
        if not candidate:
            return Response({'error': 'Candidate not found', 'status': status.HTTP_404_NOT_FOUND})

        subject = request.data.get('subject', 'Application Status Update')
        message = request.data.get('message', '')

        # Send email to candidate
        print(candidate.candidate.email)
        success = send_email_update(candidate.candidate.email, subject, message)
        if success:
            return Response({'message': 'Email sent to candidate successfully', 'status': status.HTTP_200_OK})

    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

@api_view(['PUT'])
def change_status(request):
    try:
        if request.method == 'PUT':
            response, isAuthenticated = get_company(request)

            if not isAuthenticated:
                return Response(response)

            company = response
            candidate_id = decrypt(request.data.get('id'))
            candidate = Application.objects.filter(id=candidate_id).first()
            candidate_profile = CandidateProfile.objects.filter(candidate=candidate.candidate).first()
            posting = Posting.objects.filter(id=candidate.posting.id).first()

            if not candidate:
                return Response({'error': 'Candidate not found', 'status': status.HTTP_404_NOT_FOUND})

            new_status = request.data.get('status')
            candidate.status = new_status
            candidate.save()

            context = {
                'company_name': posting.company.name,
                'first_name': candidate_profile.first_name,
                'job_title': posting.title,
            }

            email_successful, response_data = send_status_update_email(candidate, new_status, context)

            if not email_successful:
                return Response(response_data)

            return Response(response_data)
    except Exception as e:
        return Response({'error': str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
    
@api_view(['POST'])
def save_profile(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)

        company = response
        
        if request.method == 'POST':
            companyProfile = CompanyProfile.objects.filter(company = company)

            if companyProfile.exists():
                companyProfile = companyProfile.first()
            else:
                companyProfile = CompanyProfile.objects.create(company=company)
            
            companyProfile.profile_pic = request.data.get('profile_pic')
            companyProfile.tagline = request.data.get('tagline')
            companyProfile.about_us = request.data.get('about_us')
            companyProfile.save()

            return Response({'message': 'Profile Saved Successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_profile(request):
    try:
        response, isAuthenticated = get_company(request)

        if not isAuthenticated:
            return Response(response)

        company = response

        profile = CompanyProfile.objects.filter(company = company)

        if profile.exists():
            profile = profile.first()
            data = {
                'name': company.name,
                'profile_pic': profile.profile_pic,
                'tagline': profile.tagline,
                'about_us': profile.about_us,
            }
            return Response({'data': data, 'message': 'Profile Retrived successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Profile Not Found', 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)