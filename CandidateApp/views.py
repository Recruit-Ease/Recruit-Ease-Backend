from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CandidateSerializer

@api_view(['POST'])
def register_view(request):
    try:
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Candidate registered successfully', 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
