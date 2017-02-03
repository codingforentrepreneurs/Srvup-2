from django.db import models

# Create your models here.
class Video(models.Model):
    # id        = models.AutoField(primary_key=True) # 1, 2, 3, 4, 
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True)
    embed_code  = models.TextField()
    updated     = models.DateTimeField(auto_now=True) # last saved
    timestamp   = models.DateTimeField(auto_now_add=True) # time added

    def __str__(self): # __unicode__
        return self.title

    """
    @property
    def pk(self):
        return self.id
    """



'''

python manage.py makemigrations
python manage.py migrate

'''