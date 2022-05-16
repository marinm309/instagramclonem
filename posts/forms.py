from django.forms import ModelForm
from .models import Post, Comments, Story


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'file_upload', 'description']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['description']

class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = ['file_upload', 'story_length', 'story_length_custom']

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['story_length'].required = True

