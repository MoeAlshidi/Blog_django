from django.shortcuts import render,get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
  posts_query=Post.published.all()
  return render(request,'blog/post/list.html',{'posts':posts_query})


def post_details(request,id):
  post=get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
  return render(request,'blog/post/detail.html',{'post':post})
