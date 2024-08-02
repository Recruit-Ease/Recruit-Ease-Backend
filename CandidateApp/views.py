from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CandidateSerializer
from .utils import get_candidate
from RecruiterApp.models import Company
from .models import Candidate, CandidateProfile
from RecruiterApp.models import Posting, Application
from RecruiterApp.utils import decrypt, encrypt, send_status_update_email

@api_view(['POST'])
def register_view(request):
    try:
        email = request.data.get('email')
        if Company.objects.filter(email=email.lower()).exists() or Candidate.objects.filter(email=email.lower()).exists():
            return Response({'error': 'User with this email already exists ---', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Candidate registered successfully', 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout_view(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)

        candidate = response
        candidate.refresh_token = None
        candidate.save()
        return Response({'message': 'Logged out successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def home_view(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)
    
        candidate = response
        return Response({'data': {'candidate_name': candidate.name}, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to save the data candidate fills
@api_view(['POST'])
def save_application(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)
        
        candidate = response

        if request.method == 'POST':
            posting_id = decrypt(request.data.get('posting_id'))
            posting = Posting.objects.get(id=posting_id)
            if Application.objects.filter(candidate=candidate, posting=posting).exists():
                return Response({'error': 'Candidate has already applied for this posting', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            application = Application.objects.create(posting=posting, candidate=candidate)
            print("Application: ", application)

            candidateProfile = CandidateProfile.objects.filter(candidate=candidate)
            print("Candidate Profile: ", candidateProfile)
            cp = None
            if candidateProfile.exists():
                print("Candidate Profile Exists")
                cp = candidateProfile.first()
            else:
                cp = CandidateProfile.objects.create(candidate=candidate)
            
            cp.first_name = request.data.get('first_name')
            cp.last_name = request.data.get('last_name')
            cp.phone = request.data.get('phone')
            cp.address = request.data.get('address')
            cp.city = request.data.get('city')
            cp.province = request.data.get('province')
            cp.country = request.data.get('country')
            cp.postal_code = request.data.get('postal_code')
            cp.short_bio = request.data.get('short_bio')
            cp.save()

            application.legal_questions = request.data.get('legal_questions')
            application.questions = request.data.get('questions')
            application.resume = request.data.get('resume')

            application.save()
            # send_status_update_email(application, 'Application Submitted', {'candidate_name': cp.first_name, 'posting_title': posting.title, 'company_name': posting.company.name})

            return Response({'message': 'Application saved successfully', 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Error: ", e)
        # delete the application if any error occurs
        application.delete()
        return Response({'error': "Internal Server Error", 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to get the candidate data for a posting
@api_view(['GET'])
def get_application(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)

        candidate = response

        application_id = request.GET.get('application_id')

        print("Application ID: ", application_id)
        if application_id:
            try:
                application_id = decrypt(application_id)
                application = Application.objects.filter(id=application_id)
            except Exception as e:
                return Response({'error': 'Invalid application_id', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            application = Application.objects.filter(candidate=candidate)

        if application.exists():
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
                    'short_bio': candidateProfile.short_bio,
                    'resume': app.resume,
                    'legal_questions': app.legal_questions,
                    'questions': app.questions,
                    'created_at': app.created_at,
                    'status': app.status
                })
            return Response({'data': data, 'message': 'Application Data Received successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No applications found', 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def save_profile(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)

        candidate = response
        
        if request.method == 'POST':
            candidateProfile = CandidateProfile.objects.filter(candidate = candidate)

            if candidateProfile.exists():
                candidateProfile = candidateProfile.first()
            else:
                candidateProfile = CandidateProfile.objects.create(candidate=candidate)
            
            candidateProfile.first_name = request.data.get('first_name')
            candidateProfile.last_name = request.data.get('last_name')
            candidateProfile.phone = request.data.get('phone')
            candidateProfile.address = request.data.get('address')
            candidateProfile.city = request.data.get('city')
            candidateProfile.province = request.data.get('province')
            candidateProfile.country = request.data.get('country')
            candidateProfile.postal_code = request.data.get('postal_code')
            candidateProfile.short_bio = request.data.get('short_bio')
            candidateProfile.save()

            return Response({'message': 'Profile Saved Successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_profile(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)

        candidate = response

        profile = CandidateProfile.objects.filter(candidate = candidate)

        if profile.exists():
            profile = profile.first()
            data = {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'phone': profile.phone,
                'address': profile.address,
                'city': profile.city,
                'province': profile.province,
                'country': profile.country,
                'postal_code': profile.postal_code,
                'short_bio': profile.short_bio,
            }
            return Response({'data': data, 'message': 'Profile Retrived successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Profile Not Found', 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)