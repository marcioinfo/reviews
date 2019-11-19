# STANDARD LIBRARY IMPORT
from datetime import datetime, timedelta

# DJANGO LIBRARY IMPORT
from django.test import TestCase, Client
from django.utils import timezone

# THIRD PARTY IMPORT
from jwt import encode, exceptions
from rest_framework import status

# PROJECT IMPORT
import commons.exceptions as app_exceptions
from project.settings import TOKEN_SECRET, TOKEN_ALGORITHM, TOKEN_LIVING_TIME
from authentication.rules import AuthenticationRules
from authentication.services import AuthenticationServices
from authentication.models import Blacklist
from registration.services import RegistrationServices


class AuthenticationServicesAndRulesTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self._valid_user = 'admin@admin.com'
        self._valid_password = 'marceloPass1'
        self._invalid_user = 'i_am_not@valid.com'
        self._invalid_password = 'invalid123'

    def __check_if_raise_errors(self,
                                entry,
                                exception,
                                message,
                                case=None,
                                check_password=True):
        """ Check if invalid arguments raise an error

        :parameter entry: An array with lists to be tested,
                          might be an array of arrays if
                          more than one entry is tested.
                          Example: Passwords and Username

        :parameter exception: Must be an InvalidCredentialsException
                              or any TokenException

        :parameter message: The error message that will be raised.
        """

        if exception == app_exceptions.InvalidCredentialsException:
            for username in entry[0]:
                for password in entry[1]:
                    with self.subTest(i=(username, password, case)):
                        with self.assertRaisesMessage(exception, message):
                            AuthenticationServices(
                                username=username,
                                password=password
                            ).validate_credentials(
                                check_password=check_password
                            )

        else:
            for invalid_token in entry:
                with self.subTest(i=('token: ' + str(invalid_token), case)):
                    with self.assertRaisesMessage(exception, message):
                        AuthenticationServices(
                            token=invalid_token
                        ).validate_token()

    def __check_if_true(self,
                        valid_list,
                        argument,
                        case,
                        valid_argument=None,
                        check_password=True):

        if argument == 'credentials':
            for username in valid_list:
                with self.subTest(i=(username, valid_argument, case)):
                    self.assertEqual(True,
                                     AuthenticationServices(
                                         username=username,
                                         password=valid_argument
                                     ).validate_credentials(
                                         check_password=check_password
                                     )
                                     )
        # Argument = Token in this case.
        else:
            for valid_token in valid_list:
                with self.subTest(i=('token: ' + str(valid_token), case)):
                    self.assertEqual(True,
                                     AuthenticationServices(
                                         token=valid_token
                                     ).validate_token())

    def test_validate_credentials(self):
        """ Verify if the credentials (username, password) are valid

        :exception InvalidCredentialsException: For all Cases.
        """
        valid_username = ['teste@teste.com', 'teste1@teste1.com']
        invalid_username = ['fake@account.com', 'hacky@account.com']

        valid_password = ['lalalala']
        invalid_passwords = ['12', '20', '']

        self.__check_if_raise_errors(
            entry=[valid_username, invalid_passwords],
            exception=app_exceptions.InvalidCredentialsException,
            message='Invalid Credentials.',
            case='Case: Correct username and invalid password'
        )

        self.__check_if_raise_errors(
            entry=[invalid_username, valid_password],
            exception=app_exceptions.InvalidCredentialsException,
            message='Invalid Credentials.',
            case='Case: Correct password wrong username')

        self.__check_if_raise_errors(
            entry=[invalid_username, invalid_passwords],
            exception=app_exceptions.InvalidCredentialsException,
            message='Invalid Credentials.',
            case='Case: Invalid Username, Invalid Password')

        self.__check_if_true(
            valid_list=valid_username,
            valid_argument=valid_password[0],
            argument='credentials',
            case='Case: Valid username and Valid Password')

        self.__check_if_true(
            valid_list=valid_username,
            valid_argument=invalid_passwords[0],
            argument='credentials',
            case='Case: Valid username and Valid Password',
            check_password=False)

    def test_validate_token(self):
        """ Verify if the Token is valid

        :exception DecodeError: Invalid Secret Token
        :exception InvalidAlgorithmError: Invalid Algorithm Token
        :exception ExpiredSignatureError: Expired Token
        :exception InvalidIssuedAtError: iat in the future.
        """

        valid_tokens = [encode({'username': 'admin@admin.com'},
                               TOKEN_SECRET,
                               algorithm=TOKEN_ALGORITHM)]

        invalid_secrets = ['FakE_SECRET', 'SECRET',
                           'secret', 'FailSeCreT',
                           'the_wrong_secret']

        invalid_secret_tokens = [encode({'username': 'admin@admin.com'},
                                        invalid_secret,
                                        algorithm=TOKEN_ALGORITHM)
                                 for invalid_secret in
                                 invalid_secrets if
                                 invalid_secret != TOKEN_SECRET]

        all_possible_algorithms = ['HS256', 'HS384', 'HS512']

        invalid_algorithms = [algorithm for algorithm in
                              all_possible_algorithms if
                              algorithm != TOKEN_ALGORITHM]

        invalid_algorithm_tokens = [encode(
            {'username': 'admin@admin.com'},
            TOKEN_SECRET, algorithm=invalid_algorithm)
            for invalid_algorithm in invalid_algorithms]

        living_time = timedelta(seconds=TOKEN_LIVING_TIME)
        twice_living_time = timedelta(seconds=2*TOKEN_LIVING_TIME)
        five_living_time = timedelta(seconds=2*TOKEN_LIVING_TIME)
        ten_living_time = timedelta(seconds=10*TOKEN_LIVING_TIME)

        expired_payload = {
                           'username': 'admin@admin.com',
                           'iat': datetime.now() - twice_living_time,
                           'exp': datetime.now() - living_time
                           }

        no_username_payload = {'iat': datetime.now(),
                               'exp': datetime.now() + living_time
                               }

        no_username_token = [encode(no_username_payload, TOKEN_SECRET,
                                    algorithm=TOKEN_ALGORITHM)]

        expired_tokens = [encode(expired_payload, TOKEN_SECRET,
                                 algorithm=TOKEN_ALGORITHM)]

        future_payload = {
                        'username': 'admin@admin.com',
                        'iat': datetime.now() + five_living_time,
                        'exp': datetime.now() + ten_living_time
                        }

        future_tokens = [encode(future_payload,
                                TOKEN_SECRET,
                                algorithm=TOKEN_ALGORITHM)]

        blacklisted_payload = {
                               'username': 'admin@admin.com',
                               'iat': datetime.now(),
                               'exp': datetime.now() + living_time
                               }

        blacklist_token = [encode(blacklisted_payload,
                                  TOKEN_SECRET,
                                  algorithm=TOKEN_ALGORITHM)]

        AuthenticationServices(token=blacklist_token[0]).blacklist_token()

        invalid_tokens = {'invalid secret': {
                               'entry': invalid_secret_tokens,
                               'exception': exceptions.DecodeError,
                               'message': 'Signature verification failed',
                               'case': 'Case: Invalid Secret Token'},

                          'invalid algorithm':
                              {'entry': invalid_algorithm_tokens,
                               'exception': exceptions.InvalidAlgorithmError,
                               'message': 'The specified alg value '
                                          'is not allowed',
                               'case': 'Case: Invalid Algorithm Token'},

                          'expired token': {
                              'entry': expired_tokens,
                              'exception': exceptions.ExpiredSignatureError,
                              'message': 'Signature has expired',
                              'case': 'Case: Expired Token'},

                          'future token': {
                              'entry': future_tokens,
                              'exception': exceptions.InvalidIssuedAtError,
                              'message': 'Future iat is not valid.',
                              'case': 'Case: Token with iat in the future'},

                          'no username token': {
                              'entry': no_username_token,
                              'exception': app_exceptions.InvalidPayloadException,
                              'message': 'Payload does not have information '
                                         'about the user.',
                              'case': 'Case: Token without username '
                                      'in payload'},

                          'blacklisted token': {
                              'entry': blacklist_token,
                              'exception': app_exceptions.InvalidTokenException,
                              'message': 'Token was killed',
                              'case': 'Case: Token without username in payload'},
                          }

        for key in invalid_tokens:
            self.__check_if_raise_errors(
                entry=invalid_tokens[key]['entry'],
                exception=invalid_tokens[key]['exception'],
                message=invalid_tokens[key]['message'],
                case=invalid_tokens[key]['case'])

        self.__check_if_true(valid_list=valid_tokens,
                             case='Case: Token is Valid',
                             argument='token')

    def test_properties(self):

        obj1 = AuthenticationRules(username=self._valid_user,
                                   password=self._valid_password,
                                   token='token')

        obj2 = AuthenticationServices(username=self._valid_user,
                                      password=self._valid_password,
                                      new_password=self._valid_password,
                                      token='token')

        for obj in [obj1, obj2]:

            self.assertEqual(self._valid_password, obj.password)
            self.assertEqual(self._valid_user, obj.username)
            self.assertEqual('token', obj.token)

            obj.password = 'new_pass'
            obj.username = 'new@username.com'
            obj.token = 'new_token'

            self.assertEqual('new_pass', obj.password)
            self.assertEqual('new@username.com', obj.username)
            self.assertEqual('new_token', obj.token)

        obj2.new_password = ''
        self.assertEqual('', obj2.new_password)

    def test_email_exist(self):

        # Check for valid emails.
        self.assertIsNone(AuthenticationServices(
            username=self._valid_user).check_email_exist()
                          )

        # Check for invalid emails.
        with self.assertRaisesMessage(app_exceptions.InvalidEmailException,
                                      "There is no user with the "
                                      "e-mail selected."):

            AuthenticationServices(
                username=self._invalid_user
            ).check_email_exist()

    def test_login(self):

        log_in_token = AuthenticationServices(
            username=self._valid_user,
            password=self._valid_password).login()

        self.assertIsNotNone(log_in_token)


class AuthenticationViewsTest(TestCase):
    """
    Test the views from authentication APP.
    """

    def setUp(self):
        self._client = Client()
        self._valid_username = "user@test.com"
        self._valid_password = "agriness"
        self._invalid_username = "invalid@invalid.com"
        self._invalid_password = "InvalidPassword"

        self.__creates_mock_up_user(email=self._valid_username,
                                    password=self._valid_password)

        self._auth_service = AuthenticationServices(
            username=self._valid_username, password=self._valid_password)

    @staticmethod
    def __creates_mock_up_user(email, password):
        RegistrationServices(email=email, password=password).register_user()

    @staticmethod
    def __creates_mock_up_token(email):
        return AuthenticationServices(
            username=email
        ).new_token().decode('utf-8')

    @staticmethod
    def __validate_credentials(email, password):
        return AuthenticationServices(username=email, password=password)

    def __check_responses(self, valid_response, invalid_response):

        self.assertEqual(valid_response.status_code,
                         status.HTTP_200_OK)

        self.assertEqual(invalid_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def __make_id_token_requests(self, url):

        token = self._auth_service.login().decode('utf-8')
        valid_response = self._client.post(url, {'id_token': token})
        invalid_response = self._client.post(url, {'invalid_key': ''})

        return valid_response, invalid_response

    def test_LogInView(self):

        url = '/auth/login/'
        valid_data = {'email': self._valid_username,
                      'password': self._valid_password}

        invalid_data = {'email': self._invalid_username,
                        'password': self._invalid_password}

        valid_response = self._client.post(url, valid_data)
        invalid_response = self._client.post(url, invalid_data)

        self.__check_responses(valid_response, invalid_response)

    def test_LogOutView(self):

        valid_response, invalid_response = self.__make_id_token_requests(
            url='/auth/logout/')

        self.__check_responses(valid_response, invalid_response)


class AuthenticationModelsTest(TestCase):

    def setUp(self):

        # Creation of a blacklist instance.
        self._token = 'CharField'
        self._expiration = timezone.now()
        self._blacklist_instance = Blacklist(token=self._token,
                                             expiration=self._expiration)
        self._blacklist_instance.save()

    def test_Blacklist(self):

        self.assertEqual(self._blacklist_instance.__str__(),
                         'token expires at: ' + str(self._expiration))
