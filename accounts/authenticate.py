from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class customAuthenticator(ModelBackend):
    # if @ in input of user assume email otherwise assume its contact
    def authenticate(self, request, username=None, password=None):

        user = None

        if username is None:
            return None

        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(phone_number=username)
        except User.DoesNotExist:
            return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
