from django.test import SimpleTestCase
from django.urls import resolve, reverse
from main.views import LogIn, LogOut, Story, DeleteStory
class TestUrls(SimpleTestCase):
    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, LogIn)



    
    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, LogOut)

    def test_story_url_is_resolved(self):
        url = reverse("story")
        self.assertEqual(resolve(url).func, Story)

    def test_delete_url_is_resolved(self):
        url = reverse("delete_story", args=[13])
        self.assertEqual(resolve(url).func, DeleteStory)