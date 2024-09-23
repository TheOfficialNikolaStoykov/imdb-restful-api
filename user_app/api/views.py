from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_app import signals
from user_app.api.serializers import *


@extend_schema(
    request=RegistrationSerializer,
    responses={
        201: RegistrationSerializer,
        400: OpenApiResponse(description="Validation Error", response={"type": "object", "properties": {"field_name": {"type": "array", "items": {"type": "string"}}}})
    },
    description="Handles user registration and returns a token"
)
@api_view(["POST"])
def registration_view(request):
    """
    Handle user registration and return user details along with an authentication token upon successful registration.
    """
    serializer = RegistrationSerializer(data=request.data)

    data = {}

    if serializer.is_valid():
        account = serializer.save()

        data["response"] = "Registration Successful!"
        data["username"] = account.username
        data["email"] = account.email

        token = Token.objects.get(user=account).key
        data["token"] = token

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=None,
    responses={200: None},
    description="Handles user logout by deleting the authentication token"
)
@api_view(["POST"])
def logout_view(request):
    """
    Handle user logout by deleting the user's authentication token.
    """
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
