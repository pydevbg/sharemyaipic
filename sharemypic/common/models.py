from django.db import models

from sharemypic.accounts.models import SMPUser
from sharemypic.pics.models import Image


# Create your models here.
class ImageComment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(SMPUser, on_delete=models.CASCADE)



class ImageLike(models.Model):
    user = models.ForeignKey(SMPUser, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    #This ensures that a user can like an image only once and prevents duplicate likes
    class Meta:
        unique_together = ('user', 'image')