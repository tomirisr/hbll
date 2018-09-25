from django.test import TestCase
from django.test.client import Client


class TestURLS(TestCase):
    """Test various urls."""

    def setUp(self):
        """Setup data."""

    def tearDown(self):
        """Clean up data."""

    def test_urls(self):
        urls = [
            # url, expected http code
            ('/', 200),
            ('/login/', 302),  # should redirect to CAS
            ('/login', 301),  # should permanent redirect to /login/ (with /)
            ('/status/ping', 200),
            ('/status/ping/', 200),
            ('/status/health/', 200),
        ]
        client = Client()

        for url, code in urls:
            with self.subTest(url=url):
                response = client.get(url)
                location = getattr(response, 'url', '')
                msg = f'{url} -> {location} -> {response.content}'
                self.assertEquals(response.status_code, code, msg)
