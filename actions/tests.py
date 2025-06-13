from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from actions.models import UserActivityLog
from rest_framework_simplejwt.tokens import RefreshToken

class UserActivityLogTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@user.com", password="pass1234")
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_log(self):
        url = reverse('activity-list')
        response = self.client.post(url, {"action_type": "UPLOAD_FILE"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserActivityLog.objects.count(), 1)

    def test_filter_logs_by_action_type(self):
        UserActivityLog.objects.create(user=self.user, action_type="LOGIN", status="DONE")
        url = reverse('activity-list') + '?action_type=LOGIN'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_status_transition(self):
        log = UserActivityLog.objects.create(user=self.user, action_type="UPLOAD", status="PENDING")
        url = reverse('activity-transition', args=[log.id])
        response = self.client.patch(url, {"status": "DONE"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log.refresh_from_db()
        self.assertEqual(log.status, "DONE")
