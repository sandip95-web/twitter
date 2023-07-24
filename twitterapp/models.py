from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

#Create profile for the user
class Tweet(models.Model):
    user=models.ForeignKey(User,related_name="tweets",on_delete=models.DO_NOTHING)
    body=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name="tweet_likes",blank=True)
    
    
    def number_of_likes(self):
       return self.likes.count()
    
    def __str__(self):
        return(
            f"{self.user}"
            f"{self.created_at}"
            f"{self.body}"
        )

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
             related_name="followed_by",
             symmetrical=False,
             blank=True
            )
    date_modified= models.DateTimeField(User,auto_now=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to="images/")
    profile_bio=models.CharField(blank=True,null=True,max_length=100)
    twitter_link=models.CharField(blank=True,null=True,max_length=100)
    facebook_link=models.CharField(blank=True,null=True,max_length=100)
    github_link=models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
        return self.user.username
#create a profile for user automatically
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
post_save.connect(create_profile,sender=User)