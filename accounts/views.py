from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from .forms import LoginForm
from posts.models import Post, Category
from .models import *
from django.contrib.auth.models import User
from PIL import Image
from django.core.paginator import Paginator
from .forms import PostForm




# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            form = SignupForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/login")
        else:
            form = SignupForm()

    return render(request, "accounts/signup.html", {
        "form": form
    })


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def login(request):
    return auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm)(request)



@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')



@login_required
def create_post(request):


    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()

            profile = Profile.objects.get(username=request.user.username)
            profile.posts.add(post)


            return redirect('/post/'+post.slug)

    else:
        form = PostForm()


    return render(request, 'accounts/create.html', { 'form':form})



@login_required
def profile(request):
    posts = Post.objects.all().order_by("-created_at")

    try:
        profile = Profile.objects.get(username = request.user.username)
        
    except :
        profile = Profile.objects.create(username = request.user.username)
        profile.user = request.user
        profile.save()



    total_likes = 0
    for post in profile.posts.all():
        total_likes += post.liked_by.count()


    
    return render(request, "accounts/profile.html", {'profile': profile, 'total_likes':total_likes, 'posts':posts})

@login_required
def other_profile(request,slug):
    profile = Profile.objects.get(slug=slug)
    followed = False
    posts = Post.objects.all().order_by("-created_at")


    if profile.followers.filter(username = request.user.username):
        followed = True
    else:
        followed = False

    total_likes = 0
    for post in profile.posts.all():
        total_likes += post.liked_by.count()


    if profile.username == request.user.username:
        return redirect('/profile')
    else:
        return render(request, "accounts/profile.html", {'profile': profile,'total_likes':total_likes, 'followed':followed, 'posts':posts})


@login_required
def follow(request,slug):
    profile = Profile.objects.get(slug=slug)
    user = User.objects.get(username=profile.username)
    mprofile = Profile.objects.get(username=request.user.username)
    

    if profile.followers.filter(username = request.user.username):
         profile.followers.remove(request.user)
         mprofile.followings.remove(user)

    else:
        profile.followers.add(request.user)
        mprofile.followings.add(user)

    return redirect('/profile/'+slug, {'profile':profile})



@login_required
def myposts(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10) # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/myposts.html', { 'page_obj':page_obj,'posts':posts })



@login_required
def edit_post(request,slug):
    post = Post.objects.get(slug=slug)

    if post.created_by == request.user.username:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)

            if form.is_valid():
                form.save()

                return redirect('/post/'+slug)

        else:
            form = PostForm(instance=post)


        return render(request, 'accounts/edit_post.html', {'post':post, 'form':form})
    else:
        return redirect("/")


def edit_profile(request):
    profile = Profile.objects.get(username=request.user.username)
    
    if request.method == 'POST':
            bio = request.POST['bio']
            print(request.FILES)
            if 'image' in request.FILES:
                image = request.FILES['image']
                profile.bio = bio
                profile.profile_image = image
                profile.save()
                
            else:
                profile.bio = bio
                profile.save()
            
            
            return redirect('/profile')
            


    return render(request, 'accounts/editprofile.html',{'profile':profile})




