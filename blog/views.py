from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from .models import Post

import datetime

# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# Show all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html, we use template_name to set the name vs default
    context_object_name = 'posts'  # based on home class > context
    ordering = ['-date_posted']  # add sorting on how Posts get returned
    paginate_by = 5


# show posts from certain user only
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/User_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # order_by was overriden by get_queryset
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # kwargs - query param
        return Post.objects.filter(author=user).order_by('-date_posted')


# same as above but using defaults
class PostDetailView(DetailView):
    # template_name = post_detail.html <app>/<model>_<viewtype>.html
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # provide fields that we want to see in the form
    fields = ['title', 'content']
    # success_url = '/'  # if you want to point to home page after

    def form_valid(self, form):
        # override author = user who is logged in on post
        form.instance.author = self.request.user
        #  messages.success(self, f'Your content has been Posted successfully!')  # tried to, but did not work
        return super().form_valid(form)  # running default form_valid, we just need to call again after override


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # provide fields that we want to see in the form
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Check if author == user(who wants to access)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'The About Page'})

