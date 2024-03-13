from django.test import TestCase, Client
from django.urls import reverse
from main.models import *
from urllib.parse import urlencode

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='test_user', password='Test_password99!')
        # Create a test author
        self.author = Author.objects.create(authorname='test_user', user=self.user)
        self.user.is_active = True

    def test_login_endpoint(self):
        data = urlencode({"username": "test_user", "password": "Test_password99!"})
        response = self.client.post(path="http://127.0.0.1:8000/api/login/", content_type='application/x-www-form-urlencoded', data=data)
        self.assertEqual(response.content.decode(), f"Login successful, welcome {self.user}")
        self.assertIn('Login successful', response.content.decode())

    def test_logout_endpoint(self):
        response = self.client.post(reverse('logout'), content_type="text/plain", data = urlencode({}))
        self.assertEqual(response.content.decode(), 200)
        self.assertIn('Adios', response.content.decode())

    def test_post_story_endpoint(self):
        data = urlencode({"username": "test_user", "password": "Test_password99!"})
        response = self.client.post(path="http://127.0.0.1:8000/api/login/", content_type='application/x-www-form-urlencoded', data=data)
        
        data = {'headline': 'Test Headline', 'category': 'pol', 'region': 'uk', 'details': 'Test details'}
        response = self.client.post(reverse('story'), data, content_type="application/json")
        self.assertEqual(response.content.decode(), "CREATED")
        self.assertTrue(NewsStory.objects.filter(headline='Test Headline').exists())

    def test_get_stories_endpoint(self):
        # Create some test stories
        NewsStory.objects.create(headline='Test Headline 1', category='pol', region='uk', details='Test details', author=self.author)
        NewsStory.objects.create(headline='Test Headline 2', category='tech', region='eu', details='Test details', author=self.author)

        data = urlencode({'story_cat': 'pol', 'story_region': 'uk', "date": "*"})
        print(data)
        url = reverse("story") + "?" + data
        response = self.client.get(url, data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.content.decode(), 200)
        self.assertEqual(len(response.json().get('stories')), 1)

    def test_delete_story_endpoint(self):#

        data = urlencode({"username": "test_user", "password": "Test_password99!"})
        response = self.client.post(path="http://127.0.0.1:8000/api/login/", content_type='application/x-www-form-urlencoded', data=data)
        
        # Create a test story
        story = NewsStory.objects.create(headline='Test Headline', category='pol', region='uk', details='Test details', author=self.author)

        response = self.client.delete(reverse('delete_story', args=[story.pk]))
        self.assertEqual(response.content.decode(), f"Story with id: {story.pk} has been deleted")
        self.assertFalse(NewsStory.objects.filter(pk=story.pk).exists())
