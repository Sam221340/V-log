from django.urls import path

from accounts import views

urlpatterns = [


    path('signup', views.signup, name='signup'),
    path('login',views.signin,name='login'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout',views.logout_view,name='logout'),
    path('reset_password',views.forgot_password,name='reset_password')


]