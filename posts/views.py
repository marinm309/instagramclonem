from django.shortcuts import redirect, render
from .forms import PostForm, CommentForm, StoryForm
from.models import CommentTheComment, Post, Likes, Comments, CommentLikes, Story
from django.contrib.auth.decorators import login_required
from users.models import Profile, UserFollowers
import os
from django.http import JsonResponse
import re
from django.contrib import messages

@login_required(login_url='login')
def home(request):
    user = request.user.profile
    following = UserFollowers.objects.filter(follower=user.user)
    stories = []
    user_stories = Story.objects.filter(user=user)
    print(user_stories)
    if len(user_stories) > 0:
        for i in user_stories:
            stories.append(i)
            break
    for i in following:
        story = Story.objects.filter(user=i.user)
        if len(story) > 0:
            for j in story:
                stories.append(j)
                break
    all_stories = Story.objects.all()
    for i in all_stories:
        if i.time_to_delete():
            i.delete()
    lst = []
    for i in following:
        lst.append(i.user)
    posts = Post.objects.all()
    posts = Post.objects.order_by('-created')
    comments = Comments.objects.all()
    dic = {}
    user_liked = Likes.objects.filter(user=user)
    test_lst = []
    for i in user_liked:
        test_lst.append(i.post_liked.id)
    for comment in comments:
        if comment.post not in dic:
            dic[comment.post] = [comment.description]
        else:
            dic[comment.post].append(comment.description)
    context = {'posts': posts, 'comments': comments, 'following': following, 'lst': lst, 'user': user, 'dic': dic, 'test_lst': test_lst, 'stories': stories}
    return render(request, 'posts/home.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    user = request.user.profile
    profile = Profile.objects.get(user=user.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        extesion = os.path.splitext(str(request.FILES['file_upload']))[1]
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            if extesion == '.mp4':
                post.post_type = 'video'
            else:
                post.post_type = 'photo'
            post.save()
            profile.total_posts += 1
            profile.save()
            return redirect('home')
        else:
            messages.error(request, 'Incorrect file type!')
    context = {'form': form, 'user': user}
    return render(request, 'posts/create_post.html', context)

@login_required(login_url='login')
def delete_post(request, pk):
    user = request.user.profile
    post = Post.objects.get(id=pk)
    profile = Profile.objects.get(user=user.user)
    profile.total_posts -= 1
    profile.save()
    post.delete()
    return redirect(f'/profile/{user.user}')

@login_required(login_url='login')
def edit_post(request, pk):
    user = request.user.profile
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{user.user}')
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)

@login_required(login_url='login')
def like_post(request, pk):
    user = request.user.profile
    post = Post.objects.get(id=pk)
    like = Likes.objects.filter(user=user, post_liked=post)
    if len(like) == 0:
        like = Likes.objects.create(user=user, post_liked=post)
        post.user_liked = like
        post.save()
        testing = int(post.num_of_likes())
        indf = '#' + str(post.id)
        basic_indf = str(post.id)
        return JsonResponse({'likes': testing, 'indf': indf, 'basic_indf': basic_indf})
    else:
        like = Likes.objects.get(user=user, post_liked=post)
        like.delete()
        testing = int(post.num_of_likes())
        indf = '#' + str(post.id)
        basic_indf = str(post.id)
        return JsonResponse({'likes': testing, 'indf': indf, 'basic_indf': basic_indf})
        

    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def create_comment(request, pk):
    user = request.user.profile
    post = Post.objects.get(id=pk)
    description = request.POST['comment_text']
    if 'reply_comment' in str(request.POST):
        to_comment = request.POST['reply_comment']
    if description[0] == '@' and len(to_comment) > 0:
        pattern = r"(?<=@)[^ ]+"
        reply_to = re.search(pattern, description)
        reply_to = reply_to.group(0)
        comment = Comments.objects.get(id=to_comment)
        comment_the_comment = CommentTheComment.objects.create(user=user, description=description, comment=comment)
        comment_the_comment.save()
    else:
        comment = Comments.objects.create(user=user, post=post, description=description)
        comment.save()
        post.save()
    total_comments = int(post.num_of_comments())
    indf_comment = '.' + str(post.id)
    single_comment_id = str(comment.id) + '789'
    basic_indf = '#' + str(comment.id) + '789'
    return JsonResponse({'indf_comment': indf_comment, 'comments': total_comments, 'single_comment_id': single_comment_id, 'basic_indf': basic_indf})

    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def start_reply(request, pk, ck):
    user = request.user.profile
    comment = Comments.objects.get(id=ck)
    reply_to = Profile.objects.get(id=pk)
    reply_key_word = '@' + str(reply_to.username)
    return JsonResponse({'reply_key_word': reply_key_word, 'comment': comment.id})

@login_required(login_url='login')
def delete_comment(request, pk, ck):
    user = request.user.profile
    post = Post.objects.get(id=pk)
    post.save()
    comment = Comments.objects.get(id=ck)
    basic_indf = '#' + str(comment.id) + '789'
    comment.delete()
    return JsonResponse({'basic_indf': basic_indf})

    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def like_comment(request, pk):
    user = request.user.profile
    comment = Comments.objects.get(id=pk)
    like = CommentLikes.objects.filter(user=user, comment=comment)
    if len(like) == 0:
        like = CommentLikes.objects.create(user=user, comment=comment)
        comment.likes += 1
        comment.save()
        testing = int(comment.num_of_likes())
        indf = '#' + str(comment.id)
        basic_indf = str(comment.id)
        return JsonResponse({'likes': testing, 'indf': indf, 'basic_indf': basic_indf})
    else:
        like = CommentLikes.objects.get(user=user, comment=comment)
        like.delete()
        comment.likes -= 1
        comment.save()
        testing = int(comment.num_of_likes())
        indf = '#' + str(comment.id)
        basic_indf = str(comment.id)
        return JsonResponse({'likes': testing, 'indf': indf, 'basic_indf': basic_indf})

    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def single_post(request,pk):
    user = request.user.profile
    post = Post.objects.get(id=pk)
    comments = Comments.objects.filter(post=post)
    user_followers = UserFollowers.objects.filter(follower=user.user)
    liked = post.liked_by_user(request)
    
    comment_liked = CommentLikes.objects.filter(user=user)
    test_lst = []
    for i in comment_liked:
        test_lst.append(i.comment.id)
    
    lst = []
    for i in user_followers:
        lst.append(i.user)
    if len(comments) == 0:
        empty = True
    else:
        empty = False

    context = {'comments': comments, 'user': user, 'post': post, 'lst': lst, 'empty': empty, 'liked': liked, 'test_lst': test_lst}
    return render(request, 'posts/single_post.html', context)

@login_required(login_url='login')
def show_replies(request, pk):
    comment = Comments.objects.get(id=pk)
    indf = comment.id
    return JsonResponse({'indf': indf})

@login_required(login_url='login')
def delete_replies(request, pk):
    reply = CommentTheComment.objects.get(id=pk)
    indf = '#' +  str(reply.id)
    reply.delete()
    return JsonResponse({'indf': indf})

@login_required(login_url='login')
def view_story(request, pk, ck):
    current_user = request.user.profile
    user = Profile.objects.get(username=pk)
    user_stories = Story.objects.filter(user=user)
    user_stories = user_stories.order_by('created')
    first_show = ''
    for i in user_stories:
        first_show = i
        break
    modified = []
    for i in range(len(user_stories)):
        if i == 0:
            modified.append('move')
        else:
            modified.append(str(i))

    context = {'user': current_user, 'user_stories': user_stories, 'first_show': first_show, 'modified': modified}
    return render(request, 'posts/story.html', context)

@login_required(login_url='login')
def story_forward(request, pk, ck):
    current_user = request.user.profile
    user = Profile.objects.get(username=pk)
    stories = Story.objects.filter(user=user)
    stories = stories.order_by('created')
    stories = [x.id for x in stories]
    current_story = Story.objects.get(id=ck)
    index = stories.index(current_story.id)
    if len(stories) - 1 > index:
        next_story_id = stories[index + 1]
        next = Story.objects.get(id=next_story_id)
        modified = []
        for i in range(len(stories)):
            if i == index + 1:
                modified.append('move')
            else:
                modified.append(str(i))
    else:
        return redirect('home')
    
    
    context = {'first_show': next, 'modified': modified, 'user': current_user}
    return render(request, 'posts/story.html', context)

@login_required(login_url='login')
def story_backward(request, pk, ck):
    current_user = request.user.profile
    user = Profile.objects.get(username=pk)
    stories = Story.objects.filter(user=user)
    stories = stories.order_by('created')
    stories = [x.id for x in stories]
    current_story = Story.objects.get(id=ck)
    index = stories.index(current_story.id)
    if len(stories) - 1 >= index > 0:
        prev_story_id = stories[index - 1]
        prev = Story.objects.get(id=prev_story_id)
        modified = []
        for i in range(len(stories)):
            if i == index - 1:
                modified.append('move')
            else:
                modified.append(str(i))
    else:
        return redirect('home')

    context = {'first_show': prev, 'modified': modified, 'user': current_user}
    return render(request, 'posts/story.html', context)

@login_required(login_url='login')
def create_story(request):
    user = request.user.profile
    form = StoryForm()
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        extesion = os.path.splitext(str(request.FILES['file_upload']))[1]
        if form.is_valid():
            story = form.save(commit=False)
            story.user = user
            if extesion == '.mp4':
                story.story_type = 'video'
            else:
                story.story_type = 'photo'
            story.save()
            return redirect('home')
        else:
            messages.error(request, 'Incorrect file type!')
    context = {'user': user, 'form': form}
    return render(request, 'posts/create_story.html', context)
