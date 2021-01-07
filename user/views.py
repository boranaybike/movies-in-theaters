from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import EditProfile
from movies.models import Comment
from .models import *
from django.shortcuts import get_object_or_404


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    comments = Comment.objects.filter(user=user)
    if user is not None:
        can_follow = len(Follow.objects.filter(following_id=user_id,
                                               follower_id=request.user.id)) is 0 and request.user.id is not user_id
        can_unfollow = len(
            Follow.objects.filter(following_id=user_id,
                                  follower_id=request.user.id)) > 0 and request.user.id is not user_id

    followers = Follow.objects.filter(following_id=user_id)
    following = Follow.objects.filter(follower_id=user_id)

    return render(request, 'user/profile.html',
                  {'profile': profile, 'user': user, 'comments': comments, 'can_follow': can_follow,
                   'can_unfollow': can_unfollow, 'followers': followers, 'following': following, })


def edit_profile(request):
    edit_form = None
    if request.user.is_authenticated:
        for_edit = Profile.objects.filter(user=request.user).first()
        pk = for_edit.user_id
        edit_form = EditProfile(request.POST or None, request.FILES, instance=for_edit)
        if edit_form.is_valid():

            profile_edit = edit_form.save(commit=False)
            profile_edit.user = request.user
            profile_edit.save()
            return redirect('profile', user_id=pk)

    context = {
        'edit_form': edit_form,
        'isLoggedin': request.user.is_authenticated
    }
    return render(request, 'user/edit_profile.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'login successful')
            return redirect('homepage')
        else:
            messages.add_message(request, messages.ERROR, 'username or password is wrong!')
            return redirect('login')
    else:
        return render(request, 'user/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, 'loged out')
    return redirect('homepage')


def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.WARNING, 'this username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.add_message(request, messages.WARNING, 'this email already taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'user created')
                    return redirect('login')
        else:
            messages.add_message(request, messages.WARNING, 'passwords are not same')
            return redirect('register')
    else:
        return render(request, 'user/register.html')


def follow(request, following_id):
    if len(Follow.objects.filter(follower=request.user, following=User.objects.get(id=following_id))) is 0:
        Follow.objects.create(follower=request.user, following=User.objects.get(id=following_id))
    return redirect('profile', user_id=following_id)


def un_follow(request, following_id):
    following_object = get_object_or_404(Follow, following_id=following_id, follower_id=request.user.id)
    following_object.delete()
    return redirect('profile', user_id=following_id)
