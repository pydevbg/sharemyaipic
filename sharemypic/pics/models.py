from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=100)
    tagged_images = models.ManyToManyField('Image', related_name='image_tags', blank=True)

class Image(models.Model):
    MAX_TITLE_LENGTH = 100


    title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True, null=True)
    image_file = models.ImageField(upload_to='image_uploads/',)
    generation_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    tagged_images = models.ManyToManyField(Tag, related_name='tagged', blank=True)


    def can_edit(self, user):
        return user == self.user


