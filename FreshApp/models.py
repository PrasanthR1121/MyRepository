from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
     profile_pic = models.ImageField(upload_to='profile_pic', blank=True)
     portfolio_url = models.URLField(blank=True)
     user = models.OneToOneField(User, on_delete=models.CASCADE)


class register_model(models.Model):
     name = models.CharField(max_length=50)
     username = models.CharField(max_length=50)
     email = models.EmailField(unique=True)
     phone = models.IntegerField()
     password = models.CharField(max_length=50)
     gender = models.CharField(max_length=10)

     def __str__(self):
          return self.name



