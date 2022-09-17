from django.db.models import Count
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post,Comment
from taggit.models import Tag



# Create your views here.

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'



def post_list(request, tag_slug=None):
  post_list=Post.published.all()
  tag=None
  if tag_slug:
      tag=get_object_or_404(Tag,slug=tag_slug)
      post_list=post_list.filter(tags__in=[tag])
  #Pagination with 3 posts per page.
  paginator=Paginator(post_list,3)
  page_number=request.GET.get('page',1)
  try:
    posts=paginator.page(page_number)
  except PageNotAnInteger:
    posts= paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)

  return render(request,'blog/post/list.html',{'posts':posts, 'tag':tag})


def post_details(request, post, year, month, day):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    
    comments=post.comments.filter(active=True)
    form=CommentForm
    #List of similar posts
    post_tags_id=post.tags.values_list('id',flat=True)
    similar_posts= Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    

    return render(request, 'blog/post/detail.html', {'post': post,'comments':comments,'form':form,'similar_posts':similar_posts})

@require_POST
def post_comment(request,post_id):
    post=get_object_or_404(Post,status=Post.Status.PUBLISHED, id=post_id)
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post 
        comment.save()
        
    return render(request, 'blog/post/comment.html',{'post':post, 'comment':comment, 'form':form})
        
        


