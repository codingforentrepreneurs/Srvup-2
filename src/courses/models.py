from django.conf import settings
from django.db import models
from django.db.models import Prefetch, Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.
from categories.models import Category
from videos.models import Video

from .fields import PositionField
from .utils import create_slug, make_display_price


class MyCourses(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL)
    courses         = models.ManyToManyField('Course', related_name='owned', blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.courses.all().count())

    class Meta:
        verbose_name = 'My courses'
        verbose_name_plural = 'My courses'


def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyCourses.objects.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)




POS_CHOICES = (
    ('main', 'Main'),
    ('sec', 'Secondary'),
)


class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def lectures(self):
        return self.prefetch_related('lecture_set')

    def featured(self):
        return self.filter(Q(category__slug__iexact='featured')) #| Q(secondary__slug__iexact='featured'))

    def owned(self, user):
        if user.is_authenticated(): 
            qs = MyCourses.objects.filter(user=user)
        else:
            qs = MyCourses.objects.none()
        return self.prefetch_related(
                Prefetch('owned',
                        queryset=qs,
                        to_attr='is_owner'
                )
            )


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all().active()
        #return super(CourseManager, self).all()


def handle_upload(instance, filename):
    if instance.slug:
        return "%s/images/%s" %(instance.slug, filename)
    return "unknown/images/%s" %(filename)

class Course(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True) # unique = False
    image           = models.ImageField(upload_to=handle_upload, 
                            height_field='image_height', 
                            width_field='image_width',
                            blank=True, null=True)
    image_height    = models.IntegerField(blank=True, null=True)
    image_width     = models.IntegerField(blank=True, null=True)
    # category        = models.CharField(max_length=120, choices=POS_CHOICES, default='main')
    category        = models.ForeignKey(Category, related_name='primary_category', null=True, blank=True)
    secondary       = models.ManyToManyField(Category, related_name='secondary_category', blank=True)
    order           = PositionField(collection='category')
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=100)
    active          = models.BooleanField(default=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = CourseManager() # Course.objects.all()

    # newsomething = CourseManager() # Course.newsomething.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    def get_purchase_url(self):
        return reverse("courses:purchase", kwargs={"slug": self.slug})

    def display_price(self):
        return make_display_price(self.price)


def post_save_course_receiver(sender, instance, created, *args, **kwargs):
    if not instance.category in instance.secondary.all():
        instance.secondary.add(instance.category)

post_save.connect(post_save_course_receiver, sender=Course)


# limit_choices_to={'lecture__isnull': True, 'title__icontains': "Something"}

class Lecture(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video           = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    title           = models.CharField(max_length=120)
    order           = PositionField(collection='course')
    slug            = models.SlugField(blank=True) # unique = False
    free            = models.BooleanField(default=False)
    description     = models.TextField(blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('slug', 'course'),)
        ordering = ['order', 'title'] # 0 - 100 , a-z

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







