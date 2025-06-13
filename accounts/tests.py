from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User

class UserAuthTests(APITestCase):

    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            "email": "testuser@example.com",
            "phone_number": "9999999999",
            "full_name": "Test User",
            "password": "StrongPass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        user = User.objects.create_user(email="test@example.com", password="testpass")
        url = reverse('custom-login')
        response = self.client.post(url, {"email": "test@example.com", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
