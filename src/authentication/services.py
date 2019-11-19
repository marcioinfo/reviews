# STANDARD LIBRARY IMPORT
from datetime import datetime, timedelta

# DJANGO LIBRARY IMPORT
from django.utils import timezone
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

# THIRD PARTY IMPORT
from jwt import encode, decode
# PROJECT IMPORT
from .rules import AuthenticationRules
from .models import Blacklist
from project.settings import TOKEN_SECRET, TOKEN_LIVING_TIME, TOKEN_ALGORITHM
from registration.services import RegistrationServices


class AuthenticationServices:
    """ Authentication Services:

    These services aim to solve the authentication procedures:
        1 - Login
        2 - Log-out
        3 - Password Reset
    """

    def __init__(self,
                 new_password=False,
                 username='',
                 password=False,
                 token=False,
                 name=False
                 ):
        """
        :parameter username: String
        :parameter password: String
        :parameter token: String or Binary
        """
        self.username = username
        self.password = password
        self.new_password = new_password
        self.token = token
        self.name = name

    def validate_credentials(self, check_password=True):
        """ Check if Credentials are valid.

        Uses the Rules to validate a login,
        this function will Raise an InvalidCredentialsException if
        either the username or password are wrong.

        :raises InvalidCredentialsException if wrong credentials
        :returns True if input ok.
        """
        AuthenticationRules(
            username=self.username,
            password=self.password
        ).validate_credentials(
            check_password=check_password
        )

        return True

    def validate_token(self):
        """ Check if a token is valid.

        It will Throw an exception if the token is invalid.

        :parameter self._token

        :raises

            DecodeError : Raised when a token cannot be decoded
                          because it failed validation.

            InvalidAlgorithmError : Raised when specified algorithm
                                    is not recognized by PyJWT.

            InvalidTokenError : Base exception when decode()
                                fails on a token.

            InvalidIssuedAtError : Raised when a token’s iat
                                   claim is in the future.

            ExpiredSignatureError : Raised when a token’s exp
                                    claim indicates that it has expired.

        :returns the same token if it's valid token.
        """

        AuthenticationRules(token=self.token).validate_token()

        return True

    def login(self):
        """ Authorize the login if credentials are right.

        This means that a token will be sent with the username
        and email in the payload.
        """
        token = self.new_token()

        return token

    def new_token(self, living_time=TOKEN_LIVING_TIME):
        """ Token Maker

        1 - Get the username and email.
        2 - Check the actual issued at time
        3 - Get an expiration time based on the settings.
        4 - Wrap this info on a token and return it.
        """
        name = User.objects.get(username=self.username).profile.name

        payload = {
                   'email': self.username,
                   'username': self.username,
                   'name': name,
                   'iat': timezone.now(),
                   'exp': timezone.now() + timedelta(seconds=living_time)
                   }

        token = encode(payload, TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)

        return token

    def decode_token(self):
        """ Decode Token

        """

        # Validates prior decoding.
        AuthenticationRules(token=self.token).validate_token()

        payload = decode(self.token,
                         TOKEN_SECRET,
                         algorithms=[TOKEN_ALGORITHM])

        return payload

    def blacklist_token(self):
        """ Simply Send a token to the black list.

        1 - Validate current token.
        2 - get the payload
        3 - get the expiration time
        4 - send token to the blacklist
        """
        AuthenticationRules(token=self.token).validate_token()

        payload = self.decode_token()

        exp = timezone.make_aware(datetime.fromtimestamp(int(payload['exp'])))

        dead_token = Blacklist(token=self.token, expiration=exp)

        dead_token.save()

    def check_email_exist(self):

        AuthenticationRules(username=self.username).email_exist()

    def get_username_from_token(self):
        """ Get Username From Token
        """

        auth_rules = AuthenticationRules(token=self.token)

        auth_rules.validate_token()

        self._username = self.decode_token()['username']
