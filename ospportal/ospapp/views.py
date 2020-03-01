from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.contrib.auth.models import User
# from .models import Post
# from django.views.generic import (
#     ListView,
#     DetailView,
#     CreateView,
#     UpdateView,
#     DeleteView
# )


def home(request):
    # context ={
    #     'posts': Post.objects.all()
    # }
    return render(request, 'ospapp/home.html')


def about(request):
    return render(request, 'ospapp/about.html', {'title': 'About Page'})

