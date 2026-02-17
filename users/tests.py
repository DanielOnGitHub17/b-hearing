from django.test import TestCase

from django.conf import settings

# Create your tests here.


class SettingsCheck(TestCase):
    def test_email_backend(self):
        self.assertEndsWith(settings.EMAIL_BACKEND, "PowerAutomateEmailBackend")
