# STANDARD LIBRARY IMPORT
from re import match
# DJANGO LIBRARY IMPORT
from django.contrib.auth.models import User
# PROJECT IMPORT
from commons.exceptions import InvalidEmailException, InvalidPasswordException, InvalidNameException


class RegistrationRules:

    def __init__(self, email='', password='', name=''):
        self.name = name
        self.email = email
        self.length = 6
        self.password = password


    @staticmethod
    def _is_null(parameter):

        return parameter is None or len(parameter) < 1

    @staticmethod
    def _smaller_than(value, length):

        return len(value) < length

    def _password_invalid_string(self):
        """ Check if the password contains only: Letters, Numbers,
        Dashes(-) or underscores(_).
        """

        return not match(r'^[A-Za-z0-9_-]*$', self.password)

    def _email_invalid_string(self):
        """ Check if the e-mail matches a valid common email style:

            - Starts with one or more case-sensitive character,
            dashes, numbers or (._+-)

            - followed by an '@', followed by one or more case
            sensitive character or number,

            - followed by a dot, followed by a case sensitive character,
            number, or a dot.

        """

        pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        return not match(pattern, self.email)

    def _not_unique_email(self):
        """ Make a query that checks if the email has already been taken

        """
        _filter = User.objects.filter

        return (_filter(email=self.email).exists() or
                _filter(username=self.email).exists())

    def validate(self):
        """validate if the input is a valid request or not.

        :raises InvalidEmailException: When e-mail failed one or more tests.
        :raises InvalidPasswordException: When Password failed one or more tests.
        :returns: True if passed all tests, raises an exception otherwise.
        """
        if self._is_null(self.name):
            raise InvalidNameException('The name can not be empty.')

        if self._smaller_than(self.name, 3):
            raise InvalidNameException('The name should have at '
                                       'least 3 characters.')

        if self._is_null(self.email):
            raise InvalidEmailException('The E-mail can not be empty.')

        if self._is_null(self.password):
            raise InvalidPasswordException('The password can not be empty.')

        if self._smaller_than(self.password, 6):
            raise InvalidPasswordException('The password should have at least'
                                           ' 6 characters.')

        if self._password_invalid_string():
            raise InvalidPasswordException('The password should contain '
                                           'only: Letters, Numbers, '
                                           'Dashes or underscores.')

        if self._email_invalid_string():
            raise InvalidEmailException('Your e-mail is invalid, '
                                        'please enter a valid e-mail.')

        if self._not_unique_email():
            raise InvalidEmailException('This e-mail has already been taken.')

        # ---- PASSED ALL TESTS ---- #
        return True
