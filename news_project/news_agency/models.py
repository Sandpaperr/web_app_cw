from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now


class Author(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128) #store hashed password

    def save(self, *args, **kwargs):
        #create the hashed_password and pass it to the database
        to_hash = self.name + self.username + self.password
        hashed = make_password(to_hash)
        self.password = hashed
        super(Author, self).save(*args, **kwargs)

class NewsStory(models.Model):
    categories = [("pol", "Politics"), ("art", "Art"), ("tech", "Technologies"), ("trivia", "Trivial")]
    regions = [("uk", "United Kingdom"), ("eu", "European Union"), ("w", "World")]
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=30, choices=categories)
    region = models.CharField(max_length=30, choices=regions)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    details = models.CharField(max_length=128)







