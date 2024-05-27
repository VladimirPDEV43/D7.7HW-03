from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = 'header_post'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_pub'] = None
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    pk_url_kwarg = 'id'


class PostSearch(ListView):
    model = Post
    ordering = 'time_of_publication'
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'
    context_object_name = 'create'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.selection_field = 'A'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_edit.html'
    context_object_name = 'edit'


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    context_object_name = 'delete'
    success_url = reverse_lazy('news')
