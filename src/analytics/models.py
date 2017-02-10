from django.conf import settings
from django.db import models
from courses.models import Course


class CourseViewEvent(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    course  = models.ForeignKey(Course)
    views   = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.views)