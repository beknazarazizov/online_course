from django.core.mail import get_connection, EmailMessage
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from blog.models import Blog
from config import settings
from course.forms import CommentModelForm

from course.models import Course,Category,Comment
from teacher.models import Teacher

# Create your views here.


class IndexPageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.all()
        context['teacher'] = Teacher.objects.all()
        context['category'] = Category.objects.all()
        context['blog'] = Blog.objects.all()
        return context
# class IndexPageView(View):
#     def get(self, request):
#         categories = Category.objects.all()
#         teachers = Teacher.objects.all()
#         courses = Course.objects.all()
#         if categories:
#              courses = courses.filter(category_id__isnull=id)
#
#         context = {'categories': categories,
#                    'teachers': teachers,
#                    'courses': courses,
#                    'active_page': 'active'}
#         return render(request, 'home.html')
#
class CoursePage(View):
    def get(self, request):
        courses = Course.objects.all()

        context = {
                   'courses': courses,
                   }
        return render(request, 'cours/courses_page.html', context)

class CourseDetailView(TemplateView):
    template_name = 'cours/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(course_id=course)
        context.update({
            'course': course,
            'comments': comments

        })
        return context


class CategoryView(TemplateView):
    template_name = 'navbar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class ContactPage(View):
    def get(self, request):
        context = {'active_page': 'contact'}

        return render(request, 'contact/contact_page.html', context)


class AboutPage(View):
    def get(self, request):
        comments = Comment.objects.all()

        context = {'comments': comments,
                   }

        return render(request, 'about_page.html', context)

def send_email(request):
    if request.method == "POST":
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            subject = request.POST.get("subject")
            email_from = request.POST.get("email")
            recipient_list = [settings.EMAIL_HOST_USER,]
            message = request.POST.get("message")
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
        return redirect("home")

    return render(request, 'contact/contact_page.html')