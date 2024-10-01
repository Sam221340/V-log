
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,null=True,blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_image = models.ImageField(upload_to='images',null=True)
    like_by = models.ManyToManyField(User, related_name='liked_by', blank=True)
    view_counter = models.PositiveIntegerField(default=0,blank=True)
    # status = models.CharField(max_length=1, choices=(('d', 'Draft'), ('p', 'Published')), default='d')

    def __str__(self):
        return self.title


class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

