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
def get_postings(request, id=None):
    if id:
        posting_id = decrypt(id)
        postings = Posting.objects.filter(id=posting_id)
    else:
        postings = Posting.objects.filter(company=request.user)
    data = [{'id': encrypt(posting.id), 'title': posting.title, 'description': posting.description, 'company': posting.company.name, 'created_date': posting.created_at, 'is_active': posting.is_active} for posting in postings]
    return Response({'data': data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_posting(request):
    if request.method == 'POST':
        posting_id = decrypt(request.data.get('id'))
        posting = Posting.objects.get(id=posting_id)
        posting.delete()
        return Response({'data': 'Posting deleted successfully!'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_posting(request):
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