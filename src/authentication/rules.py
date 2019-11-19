# STANDARD LIBRARY IMPORT
from datetime import datetime

# DJANGO LIBRARY IMPORT
from django.utils import timezone
from django.contrib.auth.models import User

# THIRD PARTY IMPORT
from jwt import decode
from jwt.exceptions import InvalidIssuedAtError

# PROJECT IMPORT
#from .models import Blacklist

from models.models import Blacklist

from commons.exceptions import InvalidCredentialsException, \
    InvalidTokenException, InvalidEmailException, InvalidPayloadException

from project.settings import TOKEN_SECRET, TOKEN_ALGORITHM


class AuthenticationRules:
    """ Create the rules for the authentication process

    1 - Rules for Credentials Validation (Username and Password)
    2 - Rules for Tokens Validation (JWT TOKEN)
    """
    def __init__(self, username=False, password=False, token=False):
        """
        :parameter username: String
        :parameter password: String
        :parameter token: String or Binary
        """
        self.username = username
        self.password = password
        self.token = token
        self.email = username


    @staticmethod
    def _check_if_user_exists(user):

        if not User.objects.filter(username=user).exists():
            raise InvalidCredentialsException('Invalid Credentials.')

    def _check_if_password_matches(self):

        user = User.objects.get(username=self.username)
        if not user.check_password(self.password):
            raise InvalidCredentialsException('Invalid Credentials.')

    def validate_credentials(self, check_password=True):
        """ Checks if username is valid, then check if password is valid

        """

        self._check_if_user_exists(user=self.username)

        # Set a option to check the password if necessary.
        if check_password:
            self._check_if_password_matches()
        return True

    @staticmethod
    def _check_future_token(decoded):
        """ Check Future Token

        Check if a given decoded token has a future iat key.
        """
        if 'iat' in decoded:
            if timezone.make_aware(
                    datetime.fromtimestamp(int(decoded['iat']))
            ) > timezone.now():

                raise InvalidIssuedAtError('Future iat is not valid.')
            else:
                return None

    @staticmethod
    def _check_username_in_payload(decoded):

        if 'username' in decoded:
            return True
        else:
            raise InvalidPayloadException('Payload does not have '
                                          'information about the user.')

    def _check_blacklist_token(self):

        if Blacklist.objects.filter(token=self.token).exists():
            raise InvalidTokenException('Token was killed')
        else:
            return None

    def validate_token(self):
        """ Check if token is valid

        :parameter: self._token

        IT MIGHT RAISE:
        :raises
            DecodeError : Raised when a token cannot be
                          decoded because it failed validation

            InvalidAlgorithmError : Raised when specified
                                    algorithm is not recognized by PyJWT

            InvalidTokenError : Base exception when
                                decode() fails on a token

            InvalidIssuedAtError : Raised when a token’s
                                   iat claim is in the future

            ExpiredSignatureError : Raised when a token’s exp
                                    claim indicates that it has expired

            InvalidPayload: Raised when "username" is not a
                            field in the payload.

        Exceptions are handled by the middleware.

        :returns True if passed the test.
        """
        decoded = decode(self.token, TOKEN_SECRET,
                         algorithms=[TOKEN_ALGORITHM])

        self._check_future_token(decoded)
        self._check_blacklist_token()
        self._check_username_in_payload(decoded)
        self._check_if_user_exists(user=decoded.get('username'))

        return True if decoded else False

    def email_exist(self):

        if not User.objects.filter(email=self.email).exists():
            raise InvalidEmailException("There is no user with "
                                        "the e-mail selected.")
        return True
