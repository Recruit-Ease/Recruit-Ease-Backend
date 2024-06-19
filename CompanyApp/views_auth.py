from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import CompanySerializer, CompanyLoginSerializer
from .authenticate import custom_authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes

Company = get_user_model()

class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token})

class CompanyRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

class CompanyLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)