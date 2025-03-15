from django.db import models
from django.shortcuts import render, redirect,get_object_or_404
from .models import Article, LikeDislike, Advertisement, UserProfile, Message, Friendship, Comment
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from .forms import CommentForm
from django.http import JsonResponse
from django.db.models import Q,Count
from django.contrib.auth.decorators import login_required
from .utils import send_notification
from django.contrib.auth.models import User
from collections import Counter
import re


def article_list(request):
    articles = Article.objects.all().order_by('-created_at')  # Eng oxirgi maqolalar birinchi ko‘rinsin
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    article.views += 1  # O‘qilish sonini oshiramiz
    article.save()

    comments = article.comments.all()  # Izohlarni olish
    form = CommentForm(request.POST or None)


    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()

            send_notification(article.author, f"{request.user.username} maqolangizga izoh qoldirdi!", f"/article/{article.id}/")

            return redirect('article_detail', id=id)
    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments, 'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('article_list')

def like_article(request, id):
    article = get_object_or_404(Article, id=id)
    like_dislike, created = LikeDislike.objects.get_or_create(article=article, user=request.user)

    if like_dislike.like:
        like_dislike.delete()
        liked = False
    else:
        like_dislike.like = True
        like_dislike.save()
        liked = True

    return JsonResponse({"liked": liked, "likes_count": article.likes_dislikes.filter(like=True).count()})

def dislike_article(request, id):
    article = get_object_or_404(Article, id=id)
    like_dislike, created = LikeDislike.objects.get_or_create(article=article, user=request.user)

    if not like_dislike.like:
        like_dislike.delete()
        disliked = False
    else:
        like_dislike.like = False
        like_dislike.save()
        disliked = True

    return JsonResponse({"disliked": disliked, "dislikes_count": article.likes_dislikes.filter(like=False).count()})


def search_articles(request):
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        articles = Article.objects.none()

    return render(request, 'blog/search_results.html', {'articles': articles, 'query': query})

def article_list(request):
    articles = (Article.objects.all().order_by('-created_at'))
    ads = Advertisement.objects.all().order_by('-created_at')[:5]  # Eng yangi 2 ta reklamani olamiz
    return render(request, 'blog/article_list.html', {'articles': articles, 'ads': ads})

@login_required
def profile(request):
    profile = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'blog/profile.html', {'profile': profile})


@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'blog/inbox.html', {'messages': messages})


# @login_required
# def send_message(request, receiver_id):
#     receiver = get_object_or_404(User, id=receiver_id)
#     if request.method == 'POST':
#         text = request.POST['text']
#         Message.objects.create(sender=request.user, receiver=receiver, text=text)
#         return redirect('inbox')
#
#     return render(request, 'blog/send_message.html', {'receiver': receiver})


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        text = request.POST['text']
        Message.objects.create(sender=request.user, receiver=receiver, text=text)

        # Bildirishnoma yaratamiz
        send_notification(receiver, f"Sizga {request.user.username} yangi xabar yubordi!", "/inbox/")

        return redirect('inbox')

    return render(request, 'blog/send_message.html', {'receiver': receiver})


@login_required
def notifications(request):
    notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')

    # Bildirishnomalarni o‘qilgan deb belgilash
    notifications.update(is_read=True)

    return render(request, 'blog/notifications.html', {'notifications': notifications})


@login_required
def add_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    if not Friendship.objects.filter(user=request.user, friend=friend).exists():
        Friendship.objects.create(user=request.user, friend=friend)
        send_notification(friend, f"{request.user.username} sizga do‘stlik so‘rovini yubordi!", "/profile/")

    return redirect('profile')


@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    Friendship.objects.filter(user=request.user, friend=friend).delete()

    return redirect('profile')

def popular_articles(request):
    top_viewed = Article.objects.order_by('-views')[:1]  # Eng ko‘p o‘qilgan 5 ta maqola
    top_commented = Article.objects.annotate(comment_count=models.Count('comments')).order_by('-comment_count')[:1]  # Eng ko‘p izohlangan maqolalar

    return render(request, 'blog/popular_articles.html', {'top_viewed': top_viewed, 'top_commented': top_commented})


def comment_analysis(request):
    all_comments = Comment.objects.all()
    words = []

    for comment in all_comments:
        words += re.findall(r'\b\w+\b', comment.text.lower())  # Matndan so‘zlarni ajratamiz

    word_counts = Counter(words)
    top_words = word_counts.most_common(10)  # Eng ko‘p ishlatilgan 10 ta so‘z

    return render(request, 'blog/comment_analysis.html', {'top_words': top_words})