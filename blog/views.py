from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CommentForm
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post,Comment



# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'



# def post_list(request):
#   post_list=Post.published.all()
#   #Pagination with 3 posts per page.
#   paginator=Paginator(post_list,3)
#   page_number=request.GET.get('page',1)
#   try:
#     posts=paginator.page(page_number);
#   except PageNotAnInteger:
#     posts= paginator.page(1);
#   except EmptyPage:
#     posts=paginator.page(paginator.num_pages);

#   return render(request,'blog/post/list.html',{'posts':posts})


def post_details(request, post, year, month, day, ):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    
    comments=post.comments.filter(active=True)
    form=CommentForm

    return render(request, 'blog/post/detail.html', {'post': post,'comments':comments,'form':form})

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
        
        


