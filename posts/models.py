from pyexpat import model
from django.db import models
import uuid
from users.models import Profile
from django.contrib.humanize.templatetags import humanize
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    like = models.IntegerField(default=0, null=True)
    photo = models.ImageField(null=True, upload_to='posts', blank=True)
    file_upload = models.FileField(null=True, upload_to='posts', validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv','png','jpg'])])
    post_type = models.CharField(max_length=100, null=True)
    user_liked = models.ForeignKey('Likes', on_delete=models.SET_NULL, null=True)

    
    def get_date(self):
        return humanize.naturaltime(self.created)

    def num_of_posts(self, user):
        posts = Post.objects.filter(user = user)
        return len(posts)

    def num_of_likes(self):
        likes = Likes.objects.filter(post_liked = self)
        return len(likes)

    def num_of_comments(self):
        comments = Comments.objects.filter(post=self)
        return len(comments)

    def liked_by_user(self, request):
        user = request.user.profile
        liked = Likes.objects.filter(post_liked=self, user=user)
        return len(liked)

    def liked_by_user_home(self):
        liked = Likes.objects.filter(post_liked=self)
        return liked

    def __str__(self) -> str:
        return str(self.id)


class Comments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    user_liked = models.ForeignKey('CommentLikes', on_delete=models.SET_NULL, null=True)
    replies = models.ForeignKey('CommentTheComment', on_delete=models.SET_NULL, null=True)

    def num_of_likes(self):
        liked = CommentLikes.objects.filter(comment=self)
        return len(liked)

    def get_date(self):
        time = humanize.naturaltime(self.created)
        time_lst = time.split(', ')
        return time_lst[0]

    def num_of_likes(self):
        likes = CommentLikes.objects.filter(comment=self)
        return len(likes)

    def num_of_replies(self):
        replies = CommentTheComment.objects.filter(comment=self)
        return len(replies)

    def all_replies(self):
        replies_lst = CommentTheComment.objects.filter(comment=self)
        return replies_lst

    def __str__(self) -> str:
        return str(self.description)

class CommentTheComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return str(self.comment.description)

class Likes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return str(self.id)

class CommentLikes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comments, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.comment)



STORY_LENGTH = (
    (5, ('5')), 
    (10, ('10')),
    (15, ('15')),
    (20, (' 20')),
    (0, ('custom'))
)

class Story(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    story_type = models.CharField(max_length=10, null=True, blank=True)
    story_length = models.IntegerField(choices=STORY_LENGTH, null=True)
    story_length_custom = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(5), MaxValueValidator(60)])
    file_upload = models.FileField(null=True, upload_to='posts', validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv','png','jpg'])])

    def time_to_delete(self):
        time = humanize.naturaltime(self.created)
        if 'day' in str(time):
            return True
        return False

    def time_ago(self):
        return humanize.naturaltime(self.created)



    def __str__(self) -> str:
        return self.user.username
