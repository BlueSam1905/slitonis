from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from .models import *
from accounts.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.


def categories(request):
    categories = Category.objects.all()
    return render(request, 'posts/categories.html', { 'categories':categories })




def feed(request,slug):
    posts = Post.objects.all().order_by('-created_at')
    category = Category.objects.get(slug=slug)
    categories = Category.objects.all()
    paginator = Paginator(posts, 10) # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'category':category, "categories":categories}
    return render(request, 'posts/feed.html', context)





def post(request,slug):
    post = get_object_or_404(Post,slug=slug)
    author = Profile.objects.get(username=post.created_by)
    categories = Category.objects.all()
    
    if request.method == "POST":
        if 'delete' in request.POST:
            post.delete()
            return redirect("/")
        if 'deletep' in request.POST:
            post.delete()
            return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'posts/post.html', { 'post':post, 'author':author, "categories":categories})







@login_required(login_url='accounts:login')
@csrf_exempt
def like_post(request, slug):
    post = Post.objects.get(slug=slug)
    profile = Profile.objects.get(username=request.user.username)
    lp = profile.liked_posts.filter(title=post.title)


    if request.method == 'POST':
        if not lp:
            post.user_liked = True
            post.liked_by.add(request.user)
            post.save()
            

            profile.liked_posts.add(post)
            profile.save()

        elif lp:
            
            post.user_liked = False
            post.liked_by.remove(request.user)
            post.save()

            profile.liked_posts.remove(post)
            profile.save()
          


    
    return redirect("/post/"+post.slug)
    

   


@login_required
def search(request):
    posts = Post.objects.all().order_by("-created_at")
    profiles = Profile.objects.all()

    if request.method == 'POST':
        query = request.POST['search']

        

    

    return render(request, 'posts/search.html', {'query':query, 'posts':posts, 'profiles':profiles,})
