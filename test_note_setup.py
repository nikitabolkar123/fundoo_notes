import pdb
# from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestSetUp(APITestCase):

    def setUp(self):
        self.note_url = reverse('notesapiviews')
        self.note_auth_url = reverse('token_obtain_pair'),
        self.register_url = reverse('userregistration')
        self.login_url = reverse('login')
        self.label_url = reverse('label')

        self.client = APIClient()
        self.user_data = {
            "first_name": "nish",
            "last_name": "bolkar",
            "username": "nish",
            "password": "123",
            "city": "aurangabad",
            "phnno": 1234,
            "email": "niki@gmail.com"
        }
        self.login_data = {
            "username": "nish",
            "password": "123"
        }
        # response = self.client.post(self.register_url, user_data=self.user_data)
        #This send a POST request to the register_url using  the APIClient with the user_data

        self.note_data = {
            "title": "Exam",
            "description": "exam is on sunday",
            "isArchive": False,
            "isTrash": False,
            "color": "white"
        }

        self.label_data = {
            "name": "abc",

        }
        return super().setUp() # This calls the setUp method of the parent class

    def tearDown(self): # This is a method that is called after each test method is run. It tears down the test environment.
        return super().tearDown()

    def get_token(self):
        login_data = {'username': 'nish', 'password': '123'}
        response = self.client.post(self.note_auth_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['access']