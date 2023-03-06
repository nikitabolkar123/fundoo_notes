# from .test_note_setup import TestSetUp
#
#
# class TestNotes(TestSetUp):
#     def test_notes_blank_list(self):
#         token = self.get_token()
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
#         # Test retrieving a list of notes
#         response = self.client.get(self.note_url)
#         self.assertEqual(response.status_code, 200)  # Expect a successful response
#
#     def test_create_valid_note_with_jwt_auth(self):
#         token = self.get_token()
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
#         response = self.client.post(self.note_auth_url, self.note_data, format='json')
#         self.assertEqual(response.status_code, 200)