from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from blog.models import Blog

from django.shortcuts import render
from django.views import View
from blog.models import Blog
from course.forms import CommentModelForm
from course.models import Category, Comment


class BlogsView(View):

    def get(self, request):
        page = request.GET.get('page','')
        blogs = Blog.objects.all().order_by('-id')
        paginator = Paginator(blogs, 3)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {

            'page_obj': page_obj
        }
        return render(request, 'blog/blog_list.html', context)


class BlogDetailTemplateView(TemplateView):
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.get(id=kwargs['pk'])
        blog = Blog.objects.get(id=kwargs['pk'])
        context['blog'] = blog
        context['comments'] = comments
        return context

def add_comment(request, slug):
    blog= Blog.objects.get(slug=slug)
    new_comment = None
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog = blog
            new_comment.save()
            return redirect('blog_detail_detail', slug)
    context = {'blog': blog, 'comment_form': form, 'new_comment': new_comment}
    return render(request, 'blog/blog_detail.html', context)
