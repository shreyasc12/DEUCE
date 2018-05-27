from django.db import models
#from .utils import unique_slug_generator
#from django.db.models.signals import pre_save,post_save
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL
class Event(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    #attendees = models.ManyToManyField(Profile,related_name="attending_event")
    #author = models.CharField(max_length=120)
    event_name = models.CharField(max_length=200)
    sports_complex= models.CharField(max_length=200)
	#attendees = models.CharField(max_length=4096)
    sport = models.CharField(max_length=200)
    #text = models.TextField()
    Required_Players = models.IntegerField(default=0)
    Available_Players =models.IntegerField(default=0)
    #published_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    in_time = models.CharField(max_length=200)
    out_time = models.CharField(max_length=200)
    #updated = models.DateTimeField(auto_now=True)
	#status = models.BooleanField(initial = 0)

    #slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.event_name

