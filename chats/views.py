from django.http import JsonResponse
from django.shortcuts import render
from users.models import *
from posts.models import *
from . models import *
from django.http import JsonResponse
from itertools import chain
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def inbox(request):
    user = request.user.profile
    friends = UserFollowers.objects.filter(follower=user.user)
    friends = [x.user.username for x in friends]
    active = False
    chats = Chat.objects.filter(user=user.user)
    context = {'friends': friends, 'user': user, 'active': active, 'chats': chats}
    print(request.method)
    return render(request, 'chats/inbox.html', context)

@login_required(login_url='login')
def active_chat(request, pk):
    user = request.user.profile
    chat_with = Profile.objects.get(id=pk)
    active = True
    chat = Chat.objects.filter(other_user=chat_with, user=user.user)
    other_user_img = 'https://instagramclonem.s3.amazonaws.com' + '/' + str(chat_with.profile_pic)
    other_user_activity = chat_with.get_last_seen()
    if len(chat) == 0:
        Chat.objects.create(other_user=chat_with)
    chat = Chat.objects.get(other_user=chat_with, user=user.user)
    MainBubble.objects.order_by('-created')
    OtherBubble.objects.order_by('-created')
    main_user_bubbles = MainBubble.objects.filter(in_chat=chat, user=user)
    other_user_bubbles = OtherBubble.objects.filter(in_chat=chat, other=chat_with)
    merged = sorted(chain(other_user_bubbles, main_user_bubbles),key=lambda instance: instance.created)
        
    merged_messages = [x.text for x in merged]
    merged_users = []
    for i in merged:
        temp = str(i).split(' ')
        if 'MainBubble' in temp[0]:
            merged_users.append(user.username)
        else:
            merged_users.append(chat_with.username)

    return JsonResponse({'other_user_activity':other_user_activity, 'other_user_img': other_user_img, 'active': active, 'chat': chat.id, 'merged_messages': merged_messages, 'merged_users': merged_users, 'user': user.username, 'chat_with': chat_with.username})

@login_required(login_url='login')
def send_message(request):
    user = request.user.profile
    message = request.POST['message']
    other_user = request.POST['other_user']
    if len(message) > 0:
        other_user = Profile.objects.get(username=other_user)
        current_chat = Chat.objects.get(user=user.user, other_user=other_user)
        other_side_chat = Chat.objects.get(other_user=user, user=other_user.user)
        print(current_chat.user, current_chat.other_user)
        MainBubble.objects.create(text=message, user=user, in_chat=current_chat)
        OtherBubble.objects.create(text=message, other=user, in_chat=other_side_chat)

    return JsonResponse({'koza': 132})

@login_required(login_url='login')
def chat_search(request):
    user = request.user.profile
    search = request.GET['chat_search_word']
    chats = Chat.objects.filter(user=user.user)
    matches = {}
    all_in_chat = [x.other_user.username for x in chats]
    for i in chats:
        if str(search) in str(i.other_user.username):
            matches[i.other_user.username] = ''
    print(matches)
    print(all_in_chat)
    return JsonResponse({'search': search, 'matches': matches, 'all_in_chat': all_in_chat})