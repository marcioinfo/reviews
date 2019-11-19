# THIRD PARTY
from rest_framework.test import APITestCase, RequestsClient

# PROJECT IMPORTS
from authentication.services import AuthenticationServices


class RegistrationRulesTest(APITestCase):

    fixtures = ['auth_user.json',
                'profile.json',
                'review.json']

    def setUp(self):

        self.fake_token = AuthenticationServices(
            username='marcelo@example.com',
            password='tops3cr3t').login()

        self.client = RequestsClient()

    def test_get(self):
        response = self.client.get('http://localhost/reviews/',
                                   headers={'Authorization': self.fake_token})

        data = eval(response.content.decode('utf-8'))

        # At least 3. Once the tests are random, the "test_post" might
        # insert a new entry first.
        self.assertTrue(len(data) >= 3)

    def test_invalid_get(self):

        # invalid url

        response = self.client.get('http://localhost/reviews',
                                   headers={'Authorization': self.fake_token})

        data = response.status_code

        self.assertTrue(data == 404)

    def test_post(self):

        response = self.client.post('http://localhost/reviews/', json={
            "company_name": "BlurryMind",
            "rating": 5,
            "summary": "A very good Company",
            "title": "I loved it"}, headers={'Authorization': self.fake_token})

        data = eval(response.content.decode('utf-8'))

        self.assertEqual(data.get('status'), 'Your Review was stored!')

    def test_invalid_post(self):

        response = self.client.post('http://localhost/reviews/', json={
            "company_name": "",
            "rating": 5,
            "summary": "A very good Company",
            "title": "I loved it"}, headers={'Authorization': self.fake_token})

        data = eval(response.content.decode('utf-8'))

        self.assertEqual(data.get('company_name'),
                         ['This field may not be blank.'])