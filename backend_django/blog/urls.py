from django.urls import path
from . import views

urlpatterns = [
    path('',views.AllPosts.as_view(),name='posts'),
    path('posts',views.AllPosts.as_view(),name='posts'),
    path('post/<int:id>',views.PostByID.as_view(),name='postDetail'),
    path('userPost',views.UserPosts.as_view(), name='UserPost'),
    path('userPost/<int:id>',views.UserPosts.as_view(), name='UserPost'),
    path('comments/<int:id>',views.Comments.as_view(), name='Comment'),
    path('comments',views.Comments.as_view(), name='Comment')
]