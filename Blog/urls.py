"""
URL configuration for BlogSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from Blog import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('photography', views.photography,name ='photography'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('travel',views.travel,name='travel'),
    path('fashion',views.fashion,name='fashion'),
    path('createblog',views.create_blog,name='createblog'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('dislike/<int:pk>/', views.dislike_post, name='dislike_post'),
    path('post_details/<int:pk>/',views.post_detail,name='post_details'),
    path('update/blog/<int:pk>/',views.UpdatePost,name='update_post'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('posts_by_month/<int:month>/<int:year>/', views.posts_by_month, name='posts_by_month'),

    # path('january_posts',views.january_posts,name='january_posts'),
    # path('comment/<int:pk>/',views.post_comments, name='post_comment')


]
