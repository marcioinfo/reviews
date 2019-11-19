# STANDARD LIBRARY IMPORT
from datetime import timedelta

# DJANGO LIBRARY IMPORT
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# THIRD PARTY IMPORT
from jwt import encode

# PROJECT IMPORT
from .rules import RegistrationRules
from project.settings import TOKEN_SECRET, TOKEN_LIVING_TIME, TOKEN_ALGORITHM


class RegistrationServices:

    def __init__(self, email=False, name=False, password=False):

        self._email = email
        self._password = password
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def validate(self):

        RegistrationRules(name=self._name,
                          email=self._email,
                          password=self._password,
                          ).validate()

    def register_user(self):

        hashed_password = make_password(self._password)

        user = User(email=self._email,
                    username=self._email,
                    password=hashed_password)

        user.save()

        user.profile.name = self._name

        user.profile.save()

    def send_jwt(self):
        """
        Creates a JWT token using the library PyJWT.
        """

        payload = {'email': self._email,
                   'username': self._email,
                   'name': self._name,
                   'iat': timezone.now(),
                   'exp': timezone.now() + timedelta(seconds=TOKEN_LIVING_TIME)
                   }

        token = encode(payload, TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)

        return token
