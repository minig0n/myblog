from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=255)
    date_posted = models.DateTimeField()
    thumbnail_url = models.URLField(max_length=200, null=True)
    active = models.BooleanField()
    content = models.TextField()

    def __str__(self):
        return f'{self.name} ({self.date_posted})'
        
class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)
    text = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def __str__(self):
        return f'"{self.text}" - {self.author.username}'