from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(CommentLikes)
admin.site.register(CommentTheComment)
admin.site.register(Story)