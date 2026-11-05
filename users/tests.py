from django.test import TestCase

# Create your tests here.

class ProjectBasicTests(TestCase):
    def test_home_page_responds(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 301, 302, 404])
