from django.test import TestCase
from .models import User
class UserTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create(name="testuser", email="test@example.com", password="1234")
self.assertEqual(user.name, "testuser")



