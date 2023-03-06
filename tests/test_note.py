# from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from tests.test_setup import TestSetUp


class TestNotes(TestSetUp):
    def test_notes_with_blank_list(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)  # generate bearer token
        # Test retrieving a list of notes
        response = self.client.get(self.notes_url)  # WE get here list of notes
        self.assertEqual(response.status_code, 200)  # Expect a successful response

    def test_create_valid_note_with_jwt_auth(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_notes_list(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # create note
        response = self.client.post(self.notes_url, self.note_data, format='json')
        # Test retrieving a list of notes
        response = self.client.get(self.notes_url)
        self.assertEqual(response.status_code, 200)  # Expect a successful response

    def test_create_note_missing_fields(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # To Test creating a new note with missing fields
        note_data = {

            "description": "hey..good morning everyone....",
        }
        response = self.client.post(self.notes_url, note_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_note_success(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Create a note
        response = self.client.post(self.notes_url, data=self.note_data, format='json')
        note_id = response.data['data']['id']
        # To Update the note
        updated_note_data = {
            'title': 'Updated Note',
            'description': 'This is an updated note'
        }
        self.update_url = reverse('notes_apiviews', args=[note_id])
        response = self.client.put(self.update_url, data=updated_note_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_note_success(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # To Create a note
        response = self.client.post(self.notes_url, data=self.note_data, format='json')
        note_id = response.data['data']['id']
        # Test deleting an existing note
        self.delete_url = reverse('notes_apiviews', args=[note_id])
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 200)  # Expect a successful delete response
        self.assertEqual(Note.objects.count(), 0)


class TestLabels(TestSetUp):
    def test_create_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Test To creating a new label
        response = self.client.post(self.lable_url, data=self.label_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['label_name'], 'Happy Holi')

    def test_get_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.lable_url, data=self.label_data, format='json')
        response = self.client.get(self.lable_url, data=self.label_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Test creating a new label
        response = self.client.post(self.lable_url, data=self.label_data, format='json')
        label_name = response.data['data']['label_name']
        label_update_url = reverse('labels_APIViews', args=[label_name])
        updated_label_data = {
            "name": "Updated Test Label"}
        response = self.client.put(label_update_url, data=updated_label_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Test creating a new label
        response = self.client.post(self.lable_url, data=self.label_data, format='json')
        label_name = response.data['data']['label_name']
        label_delete_url = reverse('labels_APIViews', args=[label_name])
        response = self.client.delete(label_delete_url)
        self.assertEqual(response.status_code, 200)
