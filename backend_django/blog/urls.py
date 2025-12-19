from django.urls import path
from . import views

urlpatterns = [
    # Home / All Posts
    path('posts/', views.allPosts, name='posts'),
    path('createPost/', views.createPostView,name='createPostView'),

    # Post Detail
    path('post/<int:id>/', views.postByID, name='postDetail'),

    # User Posts
    path('user/posts/', views.get_user_posts, name='userPosts'),       # GET all posts of logged-in user
    path('user/posts/create/', views.create_post, name='createPost'),       # POST to create a post
    path('user/posts/edit/<int:id>/', views.update_post, name='editPost'), # POST to update a post
    path('user/posts/delete/<int:id>/', views.delete_post, name='deletePost'), # POST to delete a post

    # Comments
    path('comments/', views.get_user_comments, name='comments'),                 # GET all comments
    path('comments/create/<int:id>/', views.create_comment, name='createComment'),   # POST new comment
    path('comments/<int:id>/', views.view_comment, name='commentDetail'),   # GET single comment
    path('comments/<int:id>/edit/', views.update_comment, name='editComment'), # POST to update comment
    path('comments/<int:id>/delete/', views.delete_comment, name='deleteComment')  # GET/PUT/DELETE single comment
]
