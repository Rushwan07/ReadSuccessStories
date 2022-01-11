from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Post(models.Model):
    srn = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    content = models.TextField(default="")
    like = models.ManyToManyField(User, related_name='Posts', blank=True)
    slug = models.CharField(max_length=130)
    image = models.ImageField(upload_to='images')
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name
