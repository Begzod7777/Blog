from django.urls import path
from .views import article_list, article_detail, user_login, user_logout, like_article, dislike_article, \
    search_articles, profile, send_message, inbox, notifications, add_friend, popular_articles, comment_analysis

urlpatterns = [
    path('', article_list, name='article_list'),
    path('article/<int:id>/', article_detail, name='article_detail'),
    # path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('article/<int:id>/like/', like_article, name='like_article'),
    path('article/<int:id>/dislike/', dislike_article, name='dislike_article'),
    path('search/', search_articles, name='search_articles'),
    path('profile/', profile, name='profile'),
    path('inbox/', inbox, name='inbox'),
    path('send_message/<int:receiver_id>/', send_message, name='send_message'),
    path('notifications/', notifications, name='notifications'),
    path('add_friend/<int:id>/', add_friend, name='add_friend'),  # 🔥 YANGI YO‘NALISH
    path('popular/', popular_articles, name='popular_articles'),
    path('comment-analysis/', comment_analysis, name='comment_analysis'),

]



