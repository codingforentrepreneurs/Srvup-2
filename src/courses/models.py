from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
# Create your models here.

from videos.models import Video

from .utils import create_slug

class Course(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True) # unique = False
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=100)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})






class Lecture(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video           = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True) # unique = False
    description     = models.TextField(blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('slug', 'course'),)

    def get_absolute_url(self):
        return reverse("courses:lecture-detail", 
                kwargs={
                    "cslug": self.course.slug,
                    "lslug": self.slug,
                    }
            )






def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_video_receiver, sender=Course)
# pre_save.connect(pre_save_video_receiver, sender=Lecture)







