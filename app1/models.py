from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
   name = models.CharField(max_length=100)
   
   def __str__(self):
    return self.name


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    language = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.title



class Comment(models.Model):
    
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

