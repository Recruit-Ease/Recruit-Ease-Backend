from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from RecruiterApp.models import Company

@api_view(['POST'])
def company_login_view(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            company = Company.objects.get(email=email)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found', 'status': status.HTTP_400_BAD_REQUEST})
        
        if company.check_password(password):
            company.generate_refresh_token()
            return Response({'refresh_token': company.refresh_token, 'status': status.HTTP_200_OK})
        else:
            return Response({'error': 'Invalid Credentials', 'status': status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})