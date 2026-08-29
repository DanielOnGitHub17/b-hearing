from django.test import TestCase

from server.bhearing.settings import EMAIL_BACKEND

# Create your tests here.


class SettingsCheck(TestCase):
    def test_email_backend(self):
        pass
        # self.assertEndsWith(EMAIL_BACKEND, "PowerAutomateEmailBackend")
