from RecruiterApp.models import Company
from rest_framework import status

def get_company(request):
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return ({'error': 'Authorization token not provided', 'status':status.HTTP_400_BAD_REQUEST}, False)
        
        try:
            company = Company.objects.get(refresh_token=token)
            return (company, True)
        except Company.DoesNotExist:
            return ({'error': 'Invalid Token', 'status': status.HTTP_400_BAD_REQUEST}, False)
    except Exception as e:
        return ({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, False)