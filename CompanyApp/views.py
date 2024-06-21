from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import Posting, CandidateData
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
            title = request.data.get('title')
            description = request.data.get('description')
            company = request.user
            posting = Posting.objects.create(title=title, description=description, company=company)

            posting.form_url = f"apply/{encrypt(posting.id)}/"
            posting.save()

            return Response({'data': 'Posting created successfully!'}, status=status.HTTP_201_CREATED)

        return Response({'data': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_postings(request):
    try:
        postings = Posting.objects.filter(company=request.user)
        data = [{'id': encrypt(posting.id), 'title': posting.title, 'description': posting.description, 'company': posting.company.name, 'created_date': posting.created_at, 'is_active': posting.is_active, 'form_url': posting.form_url} for posting in postings]

        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_posting(request):
    try:
        if request.method == 'DELETE':
            posting_id = decrypt(request.data.get('id'))
            posting = Posting.objects.get(id=posting_id)
            if not posting:
                return Response({'data': 'Invalid Posting ID'}, status=status.HTTP_404_NOT_FOUND)
            
            posting.delete()
            return Response({'data': 'Posting deleted successfully!'}, status=status.HTTP_200_OK)

        return Response({'data': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_posting(request):
    try:
        if request.method == 'PUT':
            posting_id = decrypt(request.data.get('id'))
            posting = Posting.objects.get(id=posting_id)
            if not posting:
                return Response({'data': 'Invalid Posting ID'}, status=status.HTTP_404_NOT_FOUND)
            
            for field, value in request.data.items():
                if field != "id" and hasattr(posting, field):
                    setattr(posting, field, value)
            posting.save()

            return Response({'data': 'Posting updated successfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# View to get a Posting Details to Create Form
@api_view(['GET'])
@permission_classes([AllowAny])
def get_posting_details(request, id):
    try:
        posting_id = decrypt(id)
        posting = Posting.objects.get(id=posting_id, is_active=True)

        if not posting:
            return Response({'data': 'Invalid Posting ID'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'title': posting.title,
            'description': posting.description,
            'company': posting.company.name,
            'created_date': posting.created_at,
            'is_active': posting.is_active,
            'form_url': posting.form_url
        }

        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### Views for Candidate Data (CRUD)

# View to save candidate data
@api_view(['POST'])
@permission_classes([AllowAny])
def save_candidateData(request):
    try:
        if request.method == 'POST':
            posting_id = decrypt(request.POST.get('posting_id'))
            posting = Posting.objects.get(id=posting_id)
            postingForm = CandidateData.objects.create(posting=posting)
            postingForm.first_name = request.POST.get('first_name')
            postingForm.last_name = request.POST.get('last_name')
            postingForm.email = request.POST.get('email')
            postingForm.phone = request.POST.get('phone')
            postingForm.address = request.POST.get('address')
            postingForm.city = request.POST.get('city')
            postingForm.province = request.POST.get('province')
            postingForm.country = request.POST.get('country')
            postingForm.postal_code = request.POST.get('postal_code')
            postingForm.resume = request.FILES.get('resume')
            postingForm.formal_questions = request.POST.get('formal_questions')
            postingForm.behavioural_questions = request.POST.get('behavioural_questions')

            postingForm.save()

            return Response({'data': 'Candidate Data Saved Successfully!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to get a Candidate Details
@api_view(['GET'])
@permission_classes([AllowAny])
def get_candidateData(request):
    try:
        candidateData = CandidateData.objects.all()

        data = [{'id': encrypt(candidate.id), 'first_name': candidate.first_name, 'last_name': candidate.last_name, 'email': candidate.email, 'phone': candidate.phone, 'address': candidate.address, 'city': candidate.city, 'province': candidate.province, 'country': candidate.country, 'postal_code': candidate.postal_code, 'resume': candidate.resume.url, 'formal_questions': candidate.formal_questions, 'behavioural_questions': candidate.behavioural_questions, "status": candidate.status, 'created_date': candidate.created_at} for candidate in candidateData]
        
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_candidateData(request):
    try:
        if request.method == 'DELETE':
            candidateID_list = request.data.get('id')

            if not isinstance(candidateID_list, list):
                candidateID_list = [candidateID_list]
            
            print(candidateID_list)
            for candidate_id in candidateID_list:
                candidate_id = decrypt(candidate_id)
                candidate = CandidateData.objects.get(id=candidate_id)
                if not candidate:
                    return Response({'data': 'Invalid Candidate ID'}, status=status.HTTP_404_NOT_FOUND)
                
                candidate.delete()

            return Response({'data': 'Selected Candidates deleted successfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_status(request):
    try:
        if request.method == 'PUT':
            candidate_id = decrypt(request.data.get('id'))
            candidate = CandidateData.objects.get(id=candidate_id)
            if not candidate:
                return Response({'data': 'Invalid Candidate ID'}, status=status.HTTP_404_NOT_FOUND)
            
            candidate.status = request.data.get('status')
            candidate.save()

            return Response({'data': 'Candidate status updated successfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERRORs)