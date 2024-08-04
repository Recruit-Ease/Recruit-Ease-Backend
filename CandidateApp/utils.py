from rest_framework import status
from .models import Candidate, Candidatetoken

def get_candidate(request):
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return ({'error': 'Authorization token not provided', 'status':status.HTTP_400_BAD_REQUEST}, False)
        
        try:
            token_entry = Candidatetoken.objects.get(token=token, is_valid=True)
            candidate = token_entry.candidate
            return (candidate, True)
        except Candidate.DoesNotExist:
            return ({'error': 'Invalid Token', 'status': status.HTTP_400_BAD_REQUEST}, False)
    except Exception as e:
        return ({'error': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, False)