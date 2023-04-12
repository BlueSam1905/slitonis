from django.db import models
from django.contrib.auth.models import User
from posts.models import *
from django.utils.text import slugify
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=255, null=True)
    bio = models.TextField(default="no bio")
    
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    followings = models.ManyToManyField(User, related_name='following', blank=True)
    total_posts = models.IntegerField(max_length=None, null=True,default=0)
    total_likes = models.IntegerField(max_length=None, null=True,default=0)
    posts = models.ManyToManyField(Post, related_name='posts', blank=True)
    slug = models.SlugField(max_length=200, unique=True,null=True,blank=True,default="none")
    profile_image = models.ImageField(upload_to='profile_images',default='Untitled.png')
    liked_posts = models.ManyToManyField(Post, related_name='liked_posts', blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title when the object is saved
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username

    

class Liked_post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    likedby = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.title