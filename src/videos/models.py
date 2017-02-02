from django.db import models

# Create your models here.
class Video(models.Model):
    title       = models.CharField(max_length=120)
    embed_code  = models.TextField()
    updated     = models.DateTimeField(auto_now=True) # last saved
    timestamp   = models.DateTimeField(auto_now_add=True) # time added

    def __str__(self): # __unicode__
        return self.title



'''

python manage.py makemigrations
python manage.py migrate

'''