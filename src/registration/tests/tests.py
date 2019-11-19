# DJANGO LIBRARY IMPORT
from django.test import TestCase, Client

# THIRD PARTY IMPORTS
from rest_framework import status

# PROJECT IMPORT
from commons import exceptions
from registration.rules import RegistrationRules
from registration.services import RegistrationServices
from authentication.services import AuthenticationServices


class RegistrationRulesTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self._name = 'Mister Test'
        self._email = 'registration@email.com'
        self._password = 'registrationPassword123'

    @staticmethod
    def _instance(name=None, email=None, password=None):

        return RegistrationRules(name=name, email=email, password=password)

    def test_properties(self):
        instance = self._instance()

        instance.email = self._email
        instance.password = self._password
        instance.name = self._name

        self.assertEqual(instance.email, self._email)
        self.assertEqual(instance.password, self._password)
        self.assertEqual(instance.name, self._name)
        self.assertEqual(instance.length, 6)

    def _check_if_raise_errors(self,
                               invalid_list,
                               valid_arguments,
                               exception,
                               message):

        """ Check if invalid arguments raise an error

        :parameter invalid_list: An array with invalid inputs to be tested.

        :parameter valid_arguments: dictionary with valid input.

        :parameter exception: Either an InvalidEmailException or
                              InvalidPasswordException

        :parameter message: The error message that will be raised.
        """

        if exception == exceptions.InvalidEmailException:
            for invalid_argument in invalid_list:
                with self.subTest(i=invalid_argument):
                    with self.assertRaisesMessage(exception, message):
                        RegistrationRules(email=invalid_argument,
                                          password=valid_arguments['password'],
                                          name=valid_arguments['name']
                                          ).validate()

        elif exception == exceptions.InvalidPasswordException:
            for invalid_argument in invalid_list:
                with self.subTest(i=invalid_argument):
                    with self.assertRaisesMessage(exception, message):
                        RegistrationRules(email=valid_arguments['email'],
                                          password=invalid_argument,
                                          name=valid_arguments['name']
                                          ).validate()

        else:
            for invalid_argument in invalid_list:
                with self.subTest(i=invalid_argument):
                    with self.assertRaisesMessage(exception, message):
                        RegistrationRules(email=valid_arguments['email'],
                                          password=valid_arguments['password'],
                                          name=invalid_argument
                                          ).validate()

    def _check_if_true(self, valid_list, valid_arguments, argument):
        """ Check if valid arguments return True

        :parameter valid_list: An array with valid inputs to be tested.

        :parameter valid_arguments: Dict with valid inputs.

        :parameter argument: either email or password,
                             this is the argument that will be put to test.
        """

        if argument == 'email':
            for valid_email in valid_list:
                with self.subTest(i=valid_email):
                    self.assertEqual(
                        True,
                        RegistrationRules(email=valid_email,
                                          password=valid_arguments['password'],
                                          name=valid_arguments['name']
                                          ).validate())

        elif argument == 'password':
            for valid_password in valid_list:
                with self.subTest(i=valid_password):
                    self.assertEqual(
                        True,
                        RegistrationRules(email=valid_arguments['email'],
                                          password=valid_password,
                                          name=valid_arguments['name']
                                          ).validate())

        else:
            for valid_name in valid_list:
                with self.subTest(i=valid_name):
                    self.assertEqual(
                        True,
                        RegistrationRules(email=valid_arguments['email'],
                                          password=valid_arguments['password'],
                                          name=valid_name
                                          ).validate())

    def test_empty_name(self):
        """ validate() should Raise an InvalidNameException if name is empty.
        and True if name is Valid.

        :raises InvalidEmailException: 'The E-mail can not be empty.'
        """

        invalid_names = ['', None]
        valid_names = ['Marcelo', 'TestBoy', 'BadGuyName', 'Test name']
        email = 'testeXXX@teste.com'
        password = 'validPassword123'

        self._check_if_raise_errors(invalid_list=invalid_names,
                                    valid_arguments={'password': password,
                                                     'email': email},
                                    exception=exceptions.InvalidNameException,
                                    message='The name can not be empty'
                                    )
        self._check_if_true(valid_list=valid_names,
                            valid_arguments={'password': password,
                                             'email': email},
                            argument='name')

    def test_empty_email(self):
        """ validate() should Raise an InvalidEmailException if email is empty.
        and True if email is Valid.

        :raises InvalidEmailException: 'The E-mail can not be empty.'
        """
        invalid_emails = ['', None]
        valid_emails = ['1@1.com', 'testeXXX@teste.com']
        password = 'validPassword123'
        name = 'test'

        self._check_if_raise_errors(invalid_list=invalid_emails,
                                    valid_arguments={'password': password,
                                                     'name': name},
                                    exception=exceptions.InvalidEmailException,
                                    message='The E-mail can not be empty.'
                                    )

        self._check_if_true(valid_list=valid_emails,
                            valid_arguments={'password': password,
                                             'name': name},
                            argument='email')

    def test_empty_password(self):
        """ validate() should Raise an InvalidEmailException if
            password is empty.

        :raises InvalidPasswordException: 'The password can not be empty.'
        """

        invalid_passwords = ['', None]
        valid_passwords = ['valid_password123']
        email = 'valid@email.com'
        name = 'test'

        self._check_if_raise_errors(
            invalid_list=invalid_passwords,
            valid_arguments={'email': email, 'name': name},
            exception=exceptions.InvalidPasswordException,
            message='The password can not be empty.'
        )

        self._check_if_true(valid_list=valid_passwords,
                            valid_arguments={'email': email,
                                             'name': name},
                            argument='password')

    def test_small_name(self):
        """ validate() should Raise an InvalidNameException if
            name is smaller than specified.

        :raises InvalidPasswordException: 'The name should have at least 3 '
                                          'characters.'
        """
        invalid_names = ['tu', 'eu', 'he', 'it']
        valid_names = ['Marcelo', 'Dolores', 'Batman']
        email = 'valid@email.com'
        password = 'swordfish'

        self._check_if_raise_errors(invalid_list=invalid_names,
                                    valid_arguments={'email': email,
                                                     'password': password},
                                    exception=exceptions.InvalidNameException,
                                    message='The name should have at least'
                                            ' 3 characters.'
                                    )

        self._check_if_true(valid_list=valid_names,
                            valid_arguments={'email': email,
                                             'password': password},
                            argument='name')

    def test_small_password(self):
        """ validate() should Raise an InvalidEmailException
            if password is smaller than specified.

        :raises InvalidPasswordException: 'The password should have at least 6
                                           characters.'
        """
        invalid_passwords = ['12345', 'aBcDe', '1234a']
        valid_passwords = ['12345678', 'aBcDeFgH', '1234_5678']
        email = 'valid@email.com'
        name = 'test'

        self._check_if_raise_errors(
            invalid_list=invalid_passwords,
            valid_arguments={'email': email, 'name': name},
            exception=exceptions.InvalidPasswordException,
            message='The password should have at least'
                    ' 6 characters.'
        )

        self._check_if_true(valid_list=valid_passwords,
                            valid_arguments={'email': email,
                                             'name': name},
                            argument='password')

    def test_password_pattern(self):
        """ validate() should Raise an InvalidEmailException
            when the password has an forbidden character.
        """
        invalid_characters = ['!', '@', '#', '$', '€', '%', '&',
                              '*', '(', ')', '?', '/', '+']

        invalid_passwords = ['1234567' + x for x in invalid_characters]

        valid_passwords = ['1234_5678', '1234-5678', 'aAbBcCdD', '12345678910']
        email = 'valid@email.com'
        name = 'test'

        self._check_if_raise_errors(
            invalid_list=invalid_passwords,
            valid_arguments={'email': email, 'name': name},
            exception=exceptions.InvalidPasswordException,
            message='The password should contain only: Letters, '
                    'Numbers, Dashes or underscores.'
        )

        self._check_if_true(valid_list=valid_passwords,
                            valid_arguments={'email': email, 'name': name},
                            argument='password')

    def test_email_pattern(self):
        """ validate() should Raise an InvalidEmailException if
            email doesnt match the regular pattern.

        :raises InvalidEmailException: 'Your e-mail is invalid, please enter '
                                       'a valid e-mail.'
        """
        password = 'validPassword123'
        name = 'test'
        invalid_characters = ['!', '@', '#', '$', '€', '%',
                              '&', '*', '(', ')', '?', '/']

        invalid_words = ['test' + x for x in invalid_characters]

        email_wrong_ids = [x + '@test.com' for x in invalid_words]
        email_wrong_domains = ['test@' + x + '.com' for x in invalid_words]
        email_wrong_suffix = ['test@test.' + x for x in invalid_words]

        invalid_emails = (email_wrong_ids
                          + email_wrong_domains
                          + email_wrong_suffix)

        valid_emails = ['test+test-test@agriness.com',
                        'join-domain@domain.com',
                        'dot.dot@dot.com']

        self._check_if_raise_errors(invalid_list=invalid_emails,
                                    valid_arguments={'password': password,
                                                     'name': name},
                                    exception=exceptions.InvalidEmailException,
                                    message='Your e-mail is invalid, please '
                                            'enter a valid e-mail.'
                                    )

        self._check_if_true(valid_list=valid_emails,
                            valid_arguments={'password': password,
                                             'name': name},
                            argument='email')

    def test_unique_user(self):
        """ validate() should Raise an InvalidEmail Exception if
            email already corresponds to an user

        :raises InvalidEmailException: 'This e-mail has already been taken.'
        """
        # Retrieve users from the fixture.

        invalid_emails = ['admin@admin.com', 'teste@teste.com']
        valid_emails = ['admin2@admin.com', 'teste2@teste.com']

        password = '12345678'
        name = 'test'

        self._check_if_raise_errors(
            invalid_list=invalid_emails,
            valid_arguments={'password': password, 'name': name},
            exception=exceptions.InvalidEmailException,
            message='This e-mail has already been taken.'
        )

        self._check_if_true(valid_list=valid_emails,
                            valid_arguments={'password': password,
                                             'name': name},
                            argument='email')


class RegistrationServicesTest(TestCase):
    """ Test the registration services."""

    def setUp(self):
        self._name = 'Mister Test'
        self._email = 'registration@email.com'
        self._password = 'registrationPassword123'

    @staticmethod
    def __instance(name=None, email=None, password=None):
        """ Creates an instance of the Registration Service."""
        return RegistrationServices(name=name, email=email, password=password)

    def test_properties(self):
        """ Tests the common behavior of the properties."""
        # Gets a service instance.
        instance = self.__instance()
        # Sets the properties.
        instance.email = self._email
        instance.password = self._password
        instance.name = self._name

        # Verify the asserts.
        self.assertEqual(instance.email, self._email)
        self.assertEqual(instance.password, self._password)
        self.assertEqual(instance.name, self._name)

    def test_validate(self):
        """ Tests the validate service.

        Tested against:
        1 - Valid credentials -> valid: name, password and email
        2 - Invalid Credentials - > invalid: name, password or email.
        """
        # Creates a valid Instance
        valid_instance = self.__instance(name=self._name,
                                         password=self._password,
                                         email=self._email)

        # Check if the validate() returns None: Standard Behavior.
        self.assertIsNone(valid_instance.validate())

        invalid_instances = {
            'invalid_name': {'name': '',
                             'email': self._email,
                             'password': self._password,
                             'exception': exceptions.InvalidNameException},
            'invalid_email': {'name': self._name,
                              'email': 'string',
                              'password': self._password,
                              'exception': exceptions.InvalidEmailException},
            'invalid_password': {'name': self._name,
                                 'email': self._email,
                                 'password': '',
                                 'exception': exceptions.InvalidPasswordException}}

        for key, value in invalid_instances.items():

            # Creates an invalid Instance
            invalid_instance = self.__instance(name=value.get('name'),
                                               email=value.get('email'),
                                               password=value.get('password'))
            with self.assertRaises(value.get('exception')):
                invalid_instance.validate()

    def test_send_jwt(self):
        """ Test the service Send JWT

        """
        name = 'Marcelo JWT test'
        email = 'test@send.jwt.com'
        password = 'ValidPassword'

        # Register the user for this test.
        RegistrationServices(name=name,
                             email=email,
                             password=password).register_user()

        # Creates an instance.
        instance = self.__instance(name=name,
                                   password=password,
                                   email=email)

        token = instance.send_jwt()

        payload = AuthenticationServices(token=token).decode_token()

        self.assertEqual(payload.get('email'), email)


class RegistrationViewsTest(TestCase):
    """ Test the Registration App Views."""

    def setUp(self):
        self._client = Client()
        self._name = 'Marcelo'
        self._email = 'blank@new.com.br'
        self._password = 'ValidPassword'

    def test_RegisterView(self):
        """ Test the Register View

        Tested Against:
        1 - Valid Credentials.
        2 - Invalid Credential.
        """
        url = '/registration/'

        # Creates Valid data.
        valid_data = dict(name='Marcelo',
                          email='blank@new.com.br',
                          password='ValidPassword')

        # Creates Invalid data.
        invalid_data = dict(nullname=dict(name='',
                                          email=self._email,
                                          password=self._password),

                            invalid_email=dict(name=self._name,
                                               email='@invalid.com',
                                               password=self._password),

                            invalid_pass=dict(name=self._name,
                                              email=self._email,
                                              password='12345'))

        valid_response = self._client.post(url, valid_data)
        self.assertEqual(valid_response.status_code, status.HTTP_200_OK)

        for key in invalid_data:
            invalid_response = self._client.post(url, invalid_data.get(key))
            self.assertEqual(invalid_response.status_code,
                             status.HTTP_400_BAD_REQUEST)
