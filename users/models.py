from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib.humanize.templatetags import humanize

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    followers = models.ForeignKey('UserFollowers', on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/default.png')
    is_active = models.BooleanField(default=False, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)


    def num_of_followers(self):
        followers = UserFollowers.objects.filter(user=self.user.profile)
        return len(followers)
    
    def num_of_followings(self):
        followings = UserFollowers.objects.filter(follower=self.user)
        return len(followings)

    def update_last_seen(self, *args, **kwargs):
        if self.is_active:
            time = datetime.now() - timedelta(hours=3)
            self.last_seen = time
        super().save(*args, **kwargs)

    def get_last_seen(self):
        time = humanize.naturaltime(self.last_seen)
        time_lst = time.split(', ')
        return time_lst[0]

    def __str__(self) -> str:
        return str(self.user)


class UserFollowers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.follower)

