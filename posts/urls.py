from django.urls import path
from .views import post_list, post_detail,post_update,post_delete,post_create,post_detail_view,post_list_view,like_post,dislike_post,create_post,search_posts,PostListCreateView,PostDetailView

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:id>/edit/', post_update, name='post_update'),
    path('post/<int:id>/delete/', post_delete, name='post_delete'),
    path('',post_list_view, name='post_list'),
    path('post/<int:pk>/', post_detail_view, name='post_detail'),
    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('post/<int:pk>/dislike/', dislike_post, name='dislike_post'),
    path('post/new/', create_post, name='create_post'),
    path('search/', search_posts, name='search_posts'),
    path('api/posts/', PostListCreateView.as_view(), name='post_list_api'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail_api'),
]

