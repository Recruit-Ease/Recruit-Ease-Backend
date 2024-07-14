from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from .utils import get_company

@api_view(['POST'])
def register_view(request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data': serializer.data, 'message': 'Company registered successfully', 'status': status.HTTP_201_CREATED})
    
    return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def logout_view(request):
    response, isAuthenticated = get_company(request)

    if not isAuthenticated:
        return Response(response)

    company = response
    company.refresh_token = None
    company.save()
    return Response({'message': 'Logged out successfully', 'status': status.HTTP_200_OK})
    

@api_view(['GET'])
def home_view(request):
    response, isAuthenticated = get_company(request)

    if not isAuthenticated:
        return Response(response)
    
    company = response
    return Response({'data': {'company_name': company.name}, 'status': status.HTTP_200_OK})
