from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=255)
    date_posted = models.DateTimeField()
    thumbnail_url = models.URLField(max_length=200, null=True)
    active = models.BooleanField()
    content = models.TextField()

    def __str__(self):
        return f'{self.name} ({self.date_posted})'
        
