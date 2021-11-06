from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.postgres.search import SearchQuery
from django.urls import reverse
from wikodeApp.models import RegistrationApplication

# Create your tests here.

client = Client()
client.login(username="admin@wikode.com", password="123456")


# models tests
class Test(TestCase):

    def create_registration(self,
                            name="test_applicant",
                            surname="test_applicant_surname",
                            email="test@ss.com",
                            applicationText="This is an application text for registration testing",
                            applicationStatus="1"
                            ):
        return RegistrationApplication.objects.create(name=name,
                                                      surname=surname,
                                                      email=email,
                                                      applicationText=applicationText,
                                                      applicationDate=timezone.now(),
                                                      applicationStatus=applicationStatus)

    def test_registration_creation(self):
        registration = self.create_registration()
        self.assertTrue(isinstance(registration, RegistrationApplication))
        control_registration = RegistrationApplication.objects.filter(email="test@ss.com").values()
        self.assertEqual(control_registration[0].get('applicationText'), registration.applicationText)

    # view tests
    def test_registration_view(self):
        url = reverse("wikodeApp:registration")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        # self.assertIn(w.title, resp.content)

    def test_registrationRequests_view(self):
        reg_request = self.create_registration()
        url = reverse("wikodeApp:registrationRequests")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(reg_request.name, resp.content.decode('utf-8'))

    def test_login_view(self):
        url = reverse("wikodeApp:userLogin")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
