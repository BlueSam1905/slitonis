from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name_plural = ("Categories")

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True,null=True, default="none")

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title when the object is saved
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.name
    

class Post(models.Model):
    category = models.ForeignKey("Category",related_name='post', on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True,null=True)
    created_by = models.CharField(max_length=255, null =True)
    slug = models.SlugField(max_length=200, unique=True,null=True,blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True, null = True)
    created_at = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to='post_images/', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Check if the generated slug is unique, if not, add a number at the end
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{Post.objects.filter(slug__startswith=slugify(self.title)).count()}"
        super(Post, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title


