from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Comment, Category
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(approved=True).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    categories = Category.objects.all()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'categories': categories,
    })

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
    })

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(title__icontains=query).order_by('-created_at') if query else Post.objects.none()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'search_term': query,
        'categories': categories
    })

def register(request):
    if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('login')
    else:         form = UserCreationForm() 
    return render(request, 'blog/register.html', {'form': form})


