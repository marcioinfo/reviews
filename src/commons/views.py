# THIRD PARTY IMPORTS
from rest_framework.views import APIView

from django.contrib.auth.models import User

# PROJECT IMPORTS
from commons import exceptions
#from commons import exceptions
from authentication.services import AuthenticationServices
#from authentication.services import AuthenticationServices


class CustomAPIView(APIView):

    @staticmethod
    def authenticate(request):
        """
        In order to be a valid authenticated
        request, it must have a valid JWT token inside
        the request header "Authorization".

        If the token is valid, return the user id.
        else raise an exception.
        """

        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            raise exceptions.TokenNotFoundInRequest('Token not found in '
                                                    'Authorization header.')

        service = AuthenticationServices(token=token)

        if service.validate_token():

            payload = service.decode_token()
            username = payload.get('username')

            user_id = User.objects.get(username=username).id

            if not user_id:
                raise exceptions.InvalidCredentialsException('Invalid User')

            return user_id

    @staticmethod
    def request_ip(request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
