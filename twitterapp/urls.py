from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('profile_list',views.profile_list,name='profile_list'),
    path('profile/<int:pk>',views.profile,name='profile'),
    path('profile/followers/<int:pk>',views.followers,name='followers'),
    path('profile/following/<int:pk>',views.following,name='following'),
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name="logout"),
    path('register',views.register_user,name="register"),
    path('update_user',views.update_user,name="update_user"),
    path('tweet_likes/<int:pk>',views.tweet_likes,name="tweet_likes"),
    path('tweet_share/<int:pk>',views.tweet_share,name="tweet_share"),
    path('unfollow/<int:pk>',views.unfollow,name="unfollow"),
    path('follow/<int:pk>',views.follow,name="follow"),
    path('delete/<int:pk>',views.delete,name="delete"),
    path('edit/<int:pk>',views.edit,name="edit"),
    path('search_tweet',views.search_tweet,name="search_tweet"),
    path('search_user',views.search_user,name="search_user"),
]
