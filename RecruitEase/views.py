from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from RecruiterApp.models import Company
from CandidateApp.models import Candidate
import uuid

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
            return Response({'refresh_token': user.refresh_token, 'is_company': is_company, 'name': user.name, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def forgot_password_view(request):
    try:
       email = request.data.get('email')

       if Company.objects.filter(email=email).exists() or Candidate.objects.filter(email=email).exists():
           request.session[f'temp_id_{email}'] = str(uuid.uuid4())
           data = {
               'email': email,
                'temp_id': request.session[f'temp_id_{email}']
           }
           return Response({'message': 'Email Verified Successfully', 'data': data,'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
       
       return Response({'error': 'Invalid Email Address', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def reset_password(request):
    try:
        email = request.data.get('email')
        temp_id = request.data.get('temp_id')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if request.session[f'temp_id_{email}'] != temp_id:
            return Response({'error': 'Bad Request', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'error': 'Passwords do not match', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        if Company.objects.filter(email=email).exists():
            user = Company.objects.get(email=email)
        elif Candidate.objects.filter(email=email).exists():
            user = Candidate.objects.get(email=email)

        
        user.set_password(password)
        user.save()

        del request.session[f'temp_id_{email}']
        
        return Response({'message': 'Password Reset Successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
