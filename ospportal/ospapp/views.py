from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from core.models import User
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def home(request):
    context ={
        'posts': Post.objects.all()
    }
    return render(request, 'ospapp/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'ospapp/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


#for listing for particular user only
class UserPostListView(ListView):
    model = Post
    template_name = 'ospapp/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


#LoginRequiredMixin ensures that a user is login before they can call this class based view
# Secondly this class users the default djanga template naming <app>/<model>_<viewtype>.html hence we do not have to
# specify "template_name" in the class. we just have to create a template tha follows that convention, that is:
# under services/(we create a template)post(model name)_detail(viewtype).html services/post_detail.html
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#by defauls django will use our ospapp/post_detail.html
#UserPassesTestMixin makes sure the uodate services belongs to the author. we don\t want
#a services to be updated by a diffrent author
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


#this class will use a default template naming convension "post_confirm_delete" (which has been creatted under services app)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'ospapp/about.html', {'title': 'About Page'})

