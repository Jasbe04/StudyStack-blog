from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib import messages  
from django.db.models import Q
from .models import Blog, Category, Comment 

# Create your views here.
def posts_by_category(request, category_id):
    # return HttpResponse(f'Posts that belongs to category with id {category_id}')
    posts = Blog.objects.filter(status='Published', category=category_id)
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     # redirect the user to homepage
    #     return redirect('home')
    
   
    category = get_object_or_404(Category, pk=category_id)
    
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'posts_by_category.html', context)


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)

    # Comments
    comments = Comment.objects.filter(blog=single_blog)
    comment_count = comments.count()
    
    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
    }
    return render(request, 'blogs.html', context)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog_slug = comment.blog.slug 

    if request.user == comment.user or request.user.is_superuser or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('blogs', slug=blog_slug) 
    else:
        return HttpResponse("You are not authorized to delete this comment.", status=403)

def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog_slug = comment.blog.slug 

    if request.user != comment.user and not request.user.is_superuser and not request.user.is_staff:
        return HttpResponse("You are not authorized to edit this comment.", status=403)

    if request.method == 'POST':
        new_comment_text = request.POST.get('comment')
        if new_comment_text:
            comment.comment = new_comment_text
            comment.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('blogs', slug=blog_slug) 
        else:
            messages.error(request, "Comment text cannot be empty.")
    
    context = {
        'comment': comment,
    }
    return render(request, 'edit_comment.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
  
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)