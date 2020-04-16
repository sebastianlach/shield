from io import BytesIO
from django.test import TestCase, Client


class ViewsTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='guest', password='qwerty.8')

    def test_can_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_can_add_and_follow_link(self):
        response = self.client.post('/', {'url': 'https://www.google.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.context)
        self.assertIn('reference', response.context)

        response = self.client.post(
            '/references/{}/'.format(response.context['reference'].rid),
            {'password': response.context['token']}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'https://www.google.com',
            fetch_redirect_response=False
        )

    def test_can_add_and_access_file(self):
        fd = BytesIO(b'sample')
        fd.name = 'sample.txt'

        response = self.client.post('/', {'content': fd})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.context)
        self.assertIn('reference', response.context)

        response = self.client.post(
            '/references/{}/'.format(response.context['reference'].rid),
            {'password': response.context['token']}
        )
        self.assertEqual(response.status_code, 302)
