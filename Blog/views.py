import calendar

from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from verify_email.email_handler import send_verification_email
# from django.urls import reverse
# from django.views.generic import TemplateView
from django.views.generic import UpdateView

from Blog.forms import PostBlogForm, CommentForm
from Blog.models import Post, PostComments, Category

# from django.template import context
# Create your views here.



def homepage(request):
    post = Post.objects.all()
    p = Paginator(post,4)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj,'post':post}
    return render(request,'homepage.html', context)

def photography(request):
    post = Post.objects.all()
    return render(request,'photography.html',context={'post':post})

def contact(request):
    # post = Post.objects.all()
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def travel(request):
    # post = Post.objects.all()
    # travel_category = Category.objects.get(name='Travel')
    post = Post.objects.filter(category__name="Travel")
    return render(request,'travel.html',context={'post':post})

def fashion(request):
    post = Post.objects.filter(category__name="Fashion")
    return render(request, 'travel.html', context={'post': post})



def create_blog(request):
    if request.method == 'POST':
        form = PostBlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            author_image = form.cleaned_data['author_image']
            tags = form.cleaned_data['tags']

            # Access the current logged-in user
            user = request.user

            post = Post.objects.create(title=title, description=description, image=image, category_id=category, author=user,author_image=author_image)
            post.tags.set(tags)

            messages.success(request, 'Blog created successfully')

            return redirect('homepage')
        else:
            return render(request, 'createblog.html', {'form': form})
    else:
        # Handle GET request, display an empty form
        form = PostBlogForm()
        return render(request, 'createblog.html', {'form': form})


def like_post(request, pk):
    if request.user.is_authenticated:
            post = Post.objects.get(id=pk)
            if request.user in post.like_by.all():
                # post.like_by.remove(request.user)
                pass
            else:
                post.like_by.add(request.user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponse('You must be logged in to like or dislike the blog')



def dislike_post(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(id=pk)
        if request.user in post.like_by.all():
            post.like_by.remove(request.user)
        else:
            pass
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponse('You must be logged in to like or dislike the blog')


def post_detail(request, pk):
    form = CommentForm()
    post_comment = PostComments.objects.filter(post=pk)

    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return HttpResponse('Post not found')

    post.view_counter += 1
    print(post.view_counter)
    post.save()
    return render(request, 'post_details.html', {'post': post, 'form': form, 'post_comment': post_comment})


def UpdatePost(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'GET':
            form = PostBlogForm(initial={'title': post.title, 'description': post.description, 'author': post.author,
                                     'category': post.category,'image':post.image,'tags':post.tags,
                                     'author_image': post.author_image, 'tags': post.tags.all()})
            return render(request, 'update_post.html', {'form': form})
        elif request.method == 'POST':
            form = PostBlogForm(request.POST,
                            initial={'title': post.title, 'description': post.description, 'author': post.author,'image':post.image,
                                     'author_image': post.author_image,
                                     'category': post.category, 'tags': post.tags.all()})
            if form.is_valid():
                post.title = form.cleaned_data['title']
                post.description = form.cleaned_data['description']
                post.author = request.user

                post.category.id = form.cleaned_data['category']
                post.image = form.cleaned_data['image']
                post.author_image = form.cleaned_data['author_image']
                selected_tags = form.cleaned_data['tags']
                post.tags.set(selected_tags)
                post.save()

                return redirect('homepage')
            else:
                return render(request, 'post_update.html', {'form': form})


def delete_post(request, id):
    try:
        post = get_object_or_404(Post, id=id)
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    except Post.DoesNotExist:
        messages.error(request, 'Post not found.')
    except ValueError:
        messages.error(request, 'Invalid post ID.')

    return redirect('homepage')






def posts_by_month(request, month, year):
    # Filter posts for the specified month and year
    posts = Post.objects.filter(created_at__month=month, created_at__year=year)
    print(posts.count)
    return render(request, 'posts_by_month.html', {'posts': posts})