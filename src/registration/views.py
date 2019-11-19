# THIRD PARTY LIBRARY IMPORT
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# PROJECT IMPORT
from .services import RegistrationServices


class RegisterView(APIView):
    """ Validate and create a new user instance in the database.
    --------
    Receives: the parameters via Json Post (email and password)

    :raise InvalidPasswordException, InvalidEmailException
    :return A brand new token if success.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Registers a New user.
        ---
        **Request Json:**

            {
              "name": "John",
              "email": "john@example.com",
              "password": "sw0rdf1sh"
            }

        **Response Json:**

            {
              "id_token": "JWT_TOKEN",
            }
        """

        name = request.data['name']
        email = request.data['email']
        password = request.data['password']

        registration_service = RegistrationServices(name=name,
                                                    email=email,
                                                    password=password)

        registration_service.validate()
        registration_service.register_user()

        token = {'id_token': registration_service.send_jwt()}

        return Response(token, status=status.HTTP_200_OK)
