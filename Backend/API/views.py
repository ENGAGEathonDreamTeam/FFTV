# Import necessary modules
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Define an APIView for testing purposes
class TestAPIView(APIView):
    def get(self, request):
        # Handle GET request logic. Here, we are simply returning a message in the response.
        data = {'message': 'Hello, API!'}
        return Response(data)

# Define an APIView for user registration
class RegisterAPIView(APIView):
    def post(self, request, format=None):
        # Create a UserSerializer instance with the data received in the POST request
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # If the serializer is valid, save the user and create a new token for them
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                # Return the user data and token as a response
                return Response(json, status=status.HTTP_201_CREATED)
        # If the serializer is not valid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define an APIView for user login
class LoginAPIView(APIView):
    def post(self, request, format=None):
        # Extract the username and password from the data in the POST request
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        # Authenticate the user using Django's authenticate function
        user = authenticate(username=username, password=password)

        if user is not None:
            # If the user exists, get or create a token for them and return it as a response
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            # If the user does not exist or the password is wrong, return an error
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Define a custom permission class
class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow users to update their own data
        return obj == request.user

class UpdateUserAPIView(APIView):
    # Set the authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSelf]

    def get(self, request, username, format=None):
        # Find the user in the database
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to view this user
        self.check_object_permissions(self.request, user)

        # Serialize the user's data
        serializer = UserSerializer(user)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        # Extract the new data from the data in the PUT request
        new_data = request.data

        # Find the user in the database
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to update this user
        self.check_object_permissions(self.request, user)

        # Update the user's data
        serializer = UserSerializer(user, data=new_data, partial=True)  # Set partial=True to update a subset of the fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
