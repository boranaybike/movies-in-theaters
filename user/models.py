from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from movies.models import Comment


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="static/images")
    social_media_url = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username

    def get_comments(self):
        return Comment.objects.filter(user=self.user)

    def get_followers(self):
        return Follow.objects.filter(following=self.user)

    def get_followings(self):
        return Follow.objects.filter(follower=self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
