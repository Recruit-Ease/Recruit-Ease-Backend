from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CandidateSerializer
from .utils import get_candidate
from RecruiterApp.models import Company
from .models import Candidate, CandidateProfile
from RecruiterApp.models import Posting, Application
from RecruiterApp.utils import decrypt, encrypt

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
            cp.save()

            application.legal_questions = request.data.get('legal_questions')
            application.questions = request.data.get('questions')
            application.resume = request.data.get('resume')

            application.save()

            return Response({'message': 'Application saved successfully', 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Error: ", e)
        return Response({'error': "Internal Server Error", 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to get the candidate data for a posting
@api_view(['GET'])
def get_application(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)
        
        company = response
        
        id = request.GET.get('id')
        posting_id = request.GET.get('posting_id')
        if id:
            application = Application.objects.filter(id=decrypt(id))
        elif posting_id:
            application = Application.objects.filter(posting_id=decrypt(posting_id))
        else:
            application = Application.objects.filter(posting__company=company)

        data = []
        for candidate in application:
            data.append({
                'id': encrypt(candidate.id),
                'posting_id': encrypt(candidate.posting.id),
                'first_name': candidate.first_name,
                'last_name': candidate.last_name,
                'email': candidate.email,
                'phone': candidate.phone,
                'address': candidate.address,
                'city': candidate.city,
                'province': candidate.province,
                'country': candidate.country,
                'postal_code': candidate.postal_code,
                'resume': candidate.resume.url,
                'questions': candidate.questions,
                'created_at': candidate.created_at,
                'status': candidate.status
            })
        
        return Response({'data': data, 'message': 'candidate data received successfully', 'status': status.HTTP_200_OK})

    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

@api_view(['DELETE'])
def delete_application(request):
    try:
        response, isAuthenticated = get_candidate(request)

        if not isAuthenticated:
            return Response(response)
        
        company = response
        if request.method == 'DELETE':
            candidateID_list = request.data.get('id')

            if not isinstance(candidateID_list, list):
                candidateID_list = [candidateID_list]
            
            for candidate_id in candidateID_list:
                candidate_id = decrypt(candidate_id)
                candidate = Application.objects.get(id=candidate_id)
                if not candidate:
                    return Response({'error': 'Candidate not found', 'status': status.HTTP_404_NOT_FOUND})
                
                candidate.delete()

            return Response({'message': 'Selected candidates deleted successfully', 'status': status.HTTP_200_OK})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
