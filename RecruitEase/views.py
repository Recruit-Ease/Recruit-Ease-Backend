from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from RecruiterApp.models import Company
from CandidateApp.models import Candidate

@api_view(['POST'])
def company_login_view(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        is_company = None

        try:
            user = Company.objects.filter(email=email)
            if not user.exists():
                user = Candidate.objects.filter(email=email)
                if not user.exists():
                    is_company = None
                    raise Exception('Invalid Email Address')
                
                is_company = False
            else:
                is_company = True
            
            user = user[0]
        except Exception as e:
            return Response({'error': 'Invalid Email Address', 'status': status.HTTP_400_BAD_REQUEST})
        
        if user.check_password(password):
            user.generate_refresh_token()
            return Response({'refresh_token': user.refresh_token, 'is_company': is_company, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
