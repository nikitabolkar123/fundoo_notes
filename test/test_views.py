import pytest
import json
from django.urls import reverse


class TestLoginAPI:
    """
        Test Login API
    """
    @pytest.mark.django_db
    def test_response_as_login_succssful(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='7777')
        user.save()
        url = reverse('user:login')
        # Login successful
        data = {'username':'sachinpawar', 'password':123}
        response = client.post(url, data)
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'sachinpawar'


    @pytest.mark.django_db
    def test_response_as_login_failed(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='sachinpawar', password='123')
        user.save()
        url = reverse('user:login')
        # Login failed
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_validation_error(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='7777')
        user.save()
        url = reverse('auth_app:user_login')
        # Validation error
        data = {'username':'Minu', 'password':''}
        response = client.post(url, data)
        assert response.status_code == 400
