from django.shortcuts import render
from posts.models import Post, Category
from accounts.models import * 
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    
    user = request.user
    categories = Category.objects.all()

    
    followed_profiles = 0
    liked_posts = 0

    if request.user.is_authenticated:
        profile = Profile.objects.get(username=request.user.username)
        followed_users = profile.followings.all()
        liked_posts = profile.liked_posts.all().order_by('-created_at')
        followed_profiles = []

        for fu in followed_users:
            ftp = Profile.objects.get(username = fu.username)
            followed_profiles.append(ftp)
        
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   

    posts = Post.objects.all()

    

    
        

    return render(request,"core/index.html",{'posts':posts, 'user':user, 'categories':categories, 'followed_profiles': followed_profiles, "liked_posts":liked_posts, 'page_obj': page_obj})