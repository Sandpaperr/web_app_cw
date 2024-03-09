from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    authorname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.authorname}"

class NewsStory(models.Model):
    categories = [("pol", "Politics"), ("art", "Art"), ("tech", "Technologies"), ("trivia", "Trivial")]
    regions = [("uk", "United Kingdom"), ("eu", "European Union"), ("w", "World")]
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=30, choices=categories)
    region = models.CharField(max_length=30, choices=regions)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    details = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.headline}"
