from django.db import models

class Tweet(models.Model):

    name = models.CharField(max_length=30)
    screen_name = models.CharField(max_length=30, default="No name")
    profile_image_url = models.URLField(default="default_profile.png")
    text = models.TextField(max_length=200)
    retweets = models.IntegerField() 
    favourites = models.IntegerField()
    date = models.DateTimeField( ['%a %b %d %H:%M:%S +0000 %Y'] )

    def __str__(self):
        return self.screen_name