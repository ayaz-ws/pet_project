from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Post
from .forms import PostCreateForm


def home_view(request):
    return render(request, "a_website/home.html")

class PostList(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "a_website/posts.html"
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Post.objects.filter(published=True)
        return queryset

class UserPostList(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "a_website/posts.html"
    paginate_by = 5
    
    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs.get("pk")
        other_user = User.objects.get(id=other_user_id)
        if other_user == user:
            queryset = Post.objects.filter(author=user)
        else:
            queryset = Post.objects.filter(author=other_user, published=True)
        return queryset


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "a_website/post_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.view_count = self.object.view_count + 1
        self.object.save(update_fields=['view_count'])

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreate(CreateView):
    form_class = PostCreateForm
    template_name = "a_website/post_create.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        self.object = post  # обязательно!
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "a_website/post_update.html"
    fields = ["title", "body", "published"]
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Проверка: пользователь должен быть автором поста
        post = self.get_object()
        return self.request.user == post.author

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "a_website/post_delete.html"
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author