from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from subject.models import Subject
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import CommentForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "All Posts"
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(context['filter'].qs, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/user_profile.html'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))        
        context['object'] = user
        context['title'] = "u/{}".format(user.username)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(context['filter'].qs, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj 
        return context

class SubjectPostListView(ListView):
    model = Post
    template_name = 'subject/profile.html'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        sub = get_object_or_404(Subject, code=self.kwargs.get('code'))
        return Post.objects.filter(subject=sub).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sub = get_object_or_404(Subject, code=self.kwargs.get('code'))       
        context['object'] = sub
        context['title'] = "s/{}".format(sub.code)
        context['contributors'] = Post.objects.filter(subject=sub).values("author").distinct().count()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(context['filter'].qs, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj 
        return context

class PostDetailView(DetailView, FormView):
    model = Post
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, instance=request.user)
        if form.is_valid():
            Comment.objects.create(post=Post.objects.filter(id=self.kwargs.get('pk')).first(), reply=request.POST.get('reply'), user=request.user)
            messages.success(request, f'Your Comment has been posted!')
            return redirect('post-detail', self.kwargs.get('pk'))
        else:
            messages.success(request, f'Sorry, something went wrong!')
            return redirect('post-detail', self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.kwargs.get('pk')).order_by('-id')
        context['title'] = "Post Details"
        context['comments'] = comments
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment-update.html'
    fields=['reply']
    
    def get_success_url(self):
        post = self.object.post
        return reverse_lazy( 'post-detail', kwargs={'pk': post.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Comment"
        return context

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields=['subject','title','content','flare']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Post"
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields=['subject','title','content','flare']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Post Edit"
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Post"
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    
    def get_success_url(self):
        post = self.object.post
        return reverse_lazy( 'post-detail', kwargs={'pk': post.id})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Comment"
        return context

def about(request):
    return render(request, 'blog/about.html', context={'title':'About'})