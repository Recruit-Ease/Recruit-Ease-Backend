from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Posting
from .utils import encrypt, decrypt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({'detail': 'Welcome to the home page!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_posting(request):
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        company = request.user
        Posting.objects.create(title=title, description=description, company=company)
        return Response({'data': 'Posting created successfully!'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_postings(request):
    postings = Posting.objects.filter(company=request.user)
    data = [{'id': encrypt(posting.id), 'title': posting.title, 'description': posting.description, 'company': posting.company.name, 'created_date': posting.created_at} for posting in postings]
    return Response({'data': data}, status=status.HTTP_200_OK)