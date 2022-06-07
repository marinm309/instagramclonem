from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import *
from .forms import CustomUserCreationForm
from chats.models import *
from django.contrib import messages


def user_register(request):
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created!')
            return redirect('login')
    context = {'form': form}
    return render(request, 'users/register.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.object.get(username=username)
        except:
            pass
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user = Profile.objects.get(user=user)
            user.is_active = True
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorrect!')
    context = {}
    return render(request, 'users/login.html', context)


@login_required(login_url='login')
def profile(request, pk):
    user = request.user.profile
    profile = Profile.objects.get(username=pk)
    posts = Post.objects.filter(user=profile)
    total_posts = Post.num_of_posts('', profile)
    followers = UserFollowers.objects.filter(user=profile)
    total_followers = len(followers)
    following = UserFollowers.objects.filter(follower=profile.user)
    total_following = len(following)
    user_followers = UserFollowers.objects.filter(follower=user.user)
    lst = []
    for i in user_followers:
        lst.append(i.user)
    context = {'posts': posts, 'user': user, 'profile': profile, 'total_posts': total_posts, 'total_followers': total_followers, 'total_following': total_following, 'lst': lst}
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def edit_profile(request, pk):
    user = request.user.profile
    profile = Profile.objects.get(id=pk)
    if profile.id != user.user.profile.id:
        return redirect(f'/profile/{user.user}')
    profile_img_now = profile.profile_pic
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{user.user}/')
        else:
            messages.error(request, 'Incorrect file type!')

    context = {'form': form, 'user': user, 'profile_img_now': profile_img_now}
    return render(request, 'users/edit_profile.html', context)

@login_required(login_url='login')
def delete_profile(request, pk):
    user = request.user.profile
    profile = Profile.objects.get(id=pk)
    if profile.id != user.user.profile.id:
        return redirect(f'/profile/{user.user}')
    elif request.method == 'POST':
        profile.delete()
        return redirect('register')
    context = {'profile': profile, 'user': user}
    return render(request, 'users/delete_profile.html', context)

@login_required(login_url='login')
def user_logout(request):
    user = request.user.profile
    user.update_last_seen()
    user.is_active = False
    user.save()
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect('login')

@login_required(login_url='login')
def search_results_profiles(request):
    user = request.user.profile
    profile = Profile.objects.get(id=user.id)
    user_followers = UserFollowers.objects.filter(follower=profile.user)
    lst = []
    key_word = ''
    for i in user_followers:
        lst.append(i.user)
    if request.method == 'POST':
        if len(request.POST) != 0:
            key_word = request.POST['search']
            profiles = Profile.objects.filter(username__contains=key_word)
            if len(profiles) != 0:
                match = True
            else:
                match = False
        else:
            key_word = ''
            profiles = Profile.objects.filter(username__contains=key_word)
            if len(profiles) != 0:
                match = True
    else:
        profiles = Profile.objects.filter(username__contains=key_word)
        if len(profiles) != 0:
            match = True

    context = {'profiles': profiles, 'user': user, 'match': match, 'followers': user_followers, 'lst': lst, 'key': key_word}
    return render(request, 'users/search_result_profiles.html', context)


@login_required(login_url='login')
def follow(request, pk):
    user = request.user.profile
    to_follow = Profile.objects.get(id=pk)
    profile = Profile.objects.get(id=user.id)
    to_follow.total_followers += 1
    to_follow.save()
    profile.total_following += 1
    profile.save()
    possible = UserFollowers.objects.filter(user=to_follow, follower=profile.user)
    if len(possible) == 0:
        UserFollowers.objects.create(user=to_follow, follower=profile.user)
        first_chat = Chat.objects.filter(user=user.user, other_user=to_follow)
        second_chat = Chat.objects.filter(user=to_follow.user, other_user=user)
        if len(first_chat) == 0 and len(second_chat) == 0:
            Chat.objects.create(user=user.user, other_user=to_follow)
            Chat.objects.create(user=to_follow.user, other_user=user)
    else:
        form = UserFollowers.objects.get(user=to_follow, follower=profile.user)
        form.delete()
    basic_indf = str(to_follow.id)
    profile_followers = str(to_follow.num_of_followers())
    profile_followings = str(to_follow.num_of_followings())
    return JsonResponse({'basic_indf': basic_indf, 'profile_followers': profile_followers, 'profile_followings': profile_followings})
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def view_followers(request, pk):
    user = request.user.profile
    profile = Profile.objects.get(username=pk)
    followers = UserFollowers.objects.filter(user=profile)
    following = UserFollowers.objects.filter(follower=user.user)
    total_followers = len(followers)
    following_lst = []
    for i in following:
        following_lst.append(i.user.username)
    context = {'followers': followers, 'following_lst': following_lst, 'user': user, 'profile': profile, 'total_followers': total_followers}
    return render(request, 'users/view_followers.html', context)


@login_required(login_url='login')
def view_following(request, pk):
    user = request.user.profile
    profile = Profile.objects.get(username=pk)
    followers = UserFollowers.objects.filter(follower=user.user)
    following = UserFollowers.objects.filter(follower=profile.user)
    total_following = len(following)
    following_lst = []
    for i in followers:
        following_lst.append(i.user.username)
    print(following_lst)
    context = {'user': user, 'profile': profile, 'following_lst': following_lst, 'following': following, 'total_following': total_following}
    return render(request, 'users/view_following.html', context)

