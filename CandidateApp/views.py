from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CandidateSerializer
from .utils import get_candidate
from RecruiterApp.models import Company
from .models import Candidate

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