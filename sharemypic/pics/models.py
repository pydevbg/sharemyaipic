from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Image(models.Model):
    MAX_TITLE_LENGTH = 100


    title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True, null=True)
    image_file = models.ImageField(upload_to='image_uploads/',)
    generation_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')

    def can_edit(self, user):
        return user == self.user
