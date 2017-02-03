from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
# Create your models here.
class Video(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True)
    embed_code  = models.TextField()
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title

def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_video_receiver, sender=Video)



# def post_save_video_receiver(sender, instance, created, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.title) #.save()
#         instance.save()

# post_save.connect(post_save_video_receiver, sender=Video)
