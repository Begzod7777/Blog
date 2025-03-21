from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment,Category, Tag
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import generics
from .serializers import PostSerializer


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Eng yangi postlar birinchi chiqadi
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_update(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})

def post_delete(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Post yaratilgandan so‘ng ro‘yxat sahifasiga qaytish
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # Ushbu postga tegishli barcha izohlar
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=pk)

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})


def post_list_view(request):
    post_list = Post.objects.all().order_by('-id')  # Eng oxirgi postlar yuqorida
    paginator = Paginator(post_list, 5)  # Har bir sahifada 5 ta post
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)  # Agar dislike bosilgan bo'lsa, uni olib tashlash

    return redirect('post_detail', pk=pk)

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)  # Agar like bosilgan bo'lsa, uni olib tashlash

    return redirect('post_detail', pk=pk)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()  # ManyToManyField uchun alohida saqlash
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})

def search_posts(request):
    query = request.GET.get('q', '')  # Qidiruv so‘rovi
    results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)

    return render(request, 'posts/search_results.html', {'query': query, 'results': results})

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer