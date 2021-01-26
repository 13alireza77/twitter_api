from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from prof.models import UserProfile


class Twitt(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk} - {self.date}"


class Hashtag(models.Model):
    twitts = models.ManyToManyField("Twitt")
    name = models.CharField(max_length=50, unique=True)
    occurrences = models.PositiveIntegerField(default=1, null=False, blank=False, auto_created=True)
    lastupdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    twitt = models.ForeignKey("Twitt", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'twitt',)

    def __str__(self):
        return f"{self.user.email} - {self.date}"


class Retwitt(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    twitt = models.ForeignKey("Twitt", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'twitt',)

    def __str__(self):
        return f"{self.user.email} - {self.date}"


class Comment(models.Model):
    parent = models.ForeignKey("Twitt", related_name="parent", on_delete=models.CASCADE)
    twitt = models.ForeignKey("Twitt", related_name="twitt", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.parent.pk} - {self.twitt.pk}"
