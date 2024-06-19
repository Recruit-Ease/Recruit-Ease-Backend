from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from CompanyApp.serializers import CompanySerializer, CompanyLoginSerializer
from CompanyApp.authenticate import custom_authenticate
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class CompanyLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CompanyLoginSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = custom_authenticate(email=email, password=password)
            if user:
                backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend=backend)
                csrf_token = get_token(request)
                return Response({'csrf_token': csrf_token}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)