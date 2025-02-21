from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import registerserializers, ProfileSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny

class registerview(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = registerserializers(data=data)
        if serializer.is_valid():
            user = serializer.save()  # Calls the corrected create method
            return Response({
                "message": "User created successfully",
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class loginview(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        # Retrieve the user by username
        user = User.objects.filter(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            })

        # Return error if authentication fails
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# class Profileview(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         serializer = ProfileSerializer(user)
#         return Response(serializer.data)
        