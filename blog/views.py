from datetime import date

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
class HomeView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name='all_posts'

class SinglePostView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post_tags = post.tags.all()
        form = CommentForm()
        comments = post.comments.all().order_by('-id')
        stored_posts = request.session.get('stored_posts',None)
        read_later = False
        if stored_posts and post.id in stored_posts:
            read_later=True
        return render(request, 'blog/post-detail.html',
                      {'post':post,
                       'post_tags':post_tags,
                       'comments':comments,
                       'form':form,
                       'read_later':read_later})
    
    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.all().order_by('-id')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))
        
        post_tags = post.tags.all()
        form = CommentForm(request.POST)
        return render(request, 'blog/post-detail.html',
                      {'post':post,
                       'post_tags':post_tags,
                       'comments':comments,
                       'form':form})

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts',None)
        context = {'posts':None}
        if stored_posts:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
        return render(request, 'blog/stored-post.html',
                      context)
    

    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if not stored_posts:
            stored_posts = []
            
        post_id = int(request.POST['post_id'])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session['stored_posts'] = stored_posts
        return HttpResponseRedirect('/')