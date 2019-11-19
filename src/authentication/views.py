# THIRD LIBRARY IMPORTS
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# PROJECT IMPORTS
from .services import AuthenticationServices


class LogInView(APIView):
    """
    Verify if a certain credential composed
    by "username" and "password" exists in the database.

    :raise InvalidCredentialsException when login is not valid.
    :return a JWT Token when login is valid.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Retrieves a token for the user session.
        ---

        **Request Json:**

            {
              "email": "user email",
              "password": "user password",
            }

        **Response Json:**

            {
              "id_token": JWT_TOKEN,
            }
        """

        username = request.data['email']
        password = request.data['password']

        auth_service = AuthenticationServices(username=username,
                                              password=password)

        auth_service.validate_credentials()
        token = auth_service.login()

        return Response({'id_token': token}, status=status.HTTP_200_OK)


class LogOutView(APIView):
    """Log Out View.

     Once an user decides to log out, the actual token is sent to a blacklist
     so it won't be able to be used again for a while.
     """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Throws the current token into the BlackList.
        ---

        **Request Json:**

            {
              "id_token": JWT_TOKEN,
            }
        """

        token = request.data['id_token']

        auth_service = AuthenticationServices(token=token)
        auth_service.blacklist_token()

        return Response({'Status': 'Log Out Finished'},
                        status=status.HTTP_200_OK)
