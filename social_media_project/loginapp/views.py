from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from loginapp.forms import Create_New_user, Edit_Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from loginapp.models import UserProfile, Follow
from postapp.forms import Postform
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    form = Create_New_user()
    registered = False
    if request.method == 'POST':
        form = Create_New_user(data=request.POST)
        if form.is_valid():
            user=form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('loginapp:login'))
    
    dict = {'form': form, 'registered': registered, 'title':'Sign up . Social'}

    return render(request, 'loginapp/signup.html', dict)

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('postapp:home'))
    return render(request, 'loginapp/login.html', context={'title':'Login', 'form':form})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = Edit_Profile(instance=current_user)
    if request.method == 'POST':
        form = Edit_Profile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            form = Edit_Profile(instance=current_user)
            return HttpResponseRedirect(reverse('loginapp:profile'))
    return render(request, 'loginapp/profile.html', context={'form':form, 'title':'Edit Profile'})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginapp:login'))

@login_required
def user_profile(request):
    form = Postform()
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'loginapp/user.html', context={'title': 'User','form':form})

@login_required
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('loginapp:profile'))
    return render (request, 'loginapp/user_other.html', context={'user_other':user_other,'already_followed':already_followed})

@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('loginapp:user', kwargs={'username':username}))

@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('loginapp:user', kwargs={'username':username}))

