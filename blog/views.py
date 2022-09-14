from django.shortcuts import render,get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
  posts=Post.published.all()
  print(posts)
  return render(request,'blog/post/list.html',{'posts':posts})


def post_details(request,pk):
  post=get_object_or_404(Post,pk=pk,status=Post.Status.PUBLISHED)
  return render(request,'blog/post/detail.html',{'post':post})
