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

        self.email = email
        self.password = password
        self.name = name


    def validate(self):

        RegistrationRules(name=self.name,
                          email=self.email,
                          password=self.password,
                          ).validate()

    def register_user(self):

        hashed_password = make_password(self.password)

        user = User(email=self.email,
                    username=self.email,
                    password=hashed_password)

        user.save()

        user.profile.name = self.name

        user.profile.save()

    def send_jwt(self):
        """
        Creates a JWT token using the library PyJWT.
        """

        payload = {'email': self.email,
                   'username': self.email,
                   'name': self.name,
                   'iat': timezone.now(),
                   'exp': timezone.now() + timedelta(seconds=TOKEN_LIVING_TIME)
                   }

        token = encode(payload, TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)

        return token
