from django.db import models

# Create your models here.
class Video(models.Model):
    embed_code = models.TextField()

    def __str__(self): # __unicode__
        return self.embed_code



'''

python manage.py makemigrations
python manage.py migrate

'''