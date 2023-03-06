from tests.test_setup import TestSetUp


# Create your tests here.
class UserRegistrationTestCase(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        # print(response)
        self.assertEqual(response.status_code, 400)

    def test_user_registration(self):
        user_data = {
            "first_name": "rani",
            "last_name": "patil",
            "email": "rani@gmail.com",
            "address": "abc",
            "phone": "12345678",
            "username": "ranip",
            "password": "rani"
        }

        response = self.client.post(self.register_url, data=user_data)
        self.assertEqual(response.status_code, 201)

    def test_user_registration_empty_username_password(self):
        data = {
            "first_name": "rani",
            "last_name": "patil",
            "email": "rani@gmail.com",
            "address": "abc",
            "phone": "12345678",
            "username": "",
            "password": "rani"
        }
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 400)


class LoginTestCase(TestSetUp):

    def test_user_login_success(self):
        user_data = {
            "first_name": "rani",
            "last_name": "patil",
            "email": "rani@gmail.com",
            "address": "abc",
            "phone": "12345678",
            "username": "ranip",
            "password": "rani"
        }

        response = self.client.post(self.register_url, data=user_data)
        print(response.data)
        # response = self.client.post(self.register_url, data=self.data)
        login_data = {
            'username': "ranip",
            'password': "rani"
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 201)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'nisha',
            'password': '1232'
        }
        response = self.client.post(self.login_url, login_data)
        print(login_data)
        self.assertEqual(response.status_code, 400)  # we will Expect an unauthorized response

    def test_user_login_missing_fields(self):
        # to test a login with missing fields
        login_data = {
            'username': 'nisha'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 400)  # Expect a bad request response
