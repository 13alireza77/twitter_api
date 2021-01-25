from django.core.validators import RegexValidator
from django.db import models


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Twitt(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    text = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    video = models.CharField(blank=True, null=True, upload_to=user_directory_path)
    date = models.DateField(auto_now_add=True, auto_created=True)
    deleted = models.BooleanField(default=False)
    hashtags = models.ManyToManyField("Hashtag")


class Hashtag(models.Model):
    name = models.CharField(validators=RegexValidator(r"^(#\w+\s+)+$"), unique=True)
    occurrences = models.IntegerField(default=0, null=False, blank=False, auto_created=True)
    lastupdate = date = models.DateField(auto_now_add=True, auto_created=True)


class Like(models.Model):
    users = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    tweet = models.ForeignKey("Twitt", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_created=True)


class Retweet(models.Model):
    users = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    tweet = models.ForeignKey("Twitt", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_created=True)
