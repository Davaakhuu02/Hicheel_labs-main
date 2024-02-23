from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Post

def index(request):
    posts_list = Post.objects.all()

    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'posts': posts})