import pdb
# from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestSetUp(APITestCase):

    def setUp(self):
        self.notes_url = reverse('notesapiviews')
        self.register_url = reverse('userregistration')
        self.login_url = reverse('login')
        self.token_url = reverse('token_obtain_pair')
        self.lable_url = reverse('labelsAPIViews')
#update table_name set fisrt_name=%s where id=%s

        self.client = APIClient()
        data = {
            "first_name": "nish",
            "last_name": "Raj",
            "email": "nish@gmail.com",
            "address": "abcd",
            "phone": "1234567",
            "username": "nisha",
            "password": "123"
        }
        response = self.client.post(self.register_url, data=data)

        self.note_data = {
            "title": "Holi",
            "description": "Avoid Synthetic Color",
            "isArchive": False,
            "isTrash": False,
            "color": "pink"
        }

        self.label_data = {
            "label_name": "Happy Holi",

        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def get_token(self):
        login_data = {'username': 'nisha', 'password': '123'}
        response = self.client.post(self.token_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['access']