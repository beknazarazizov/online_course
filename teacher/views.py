from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from django.views import View
from django.views.generic import TemplateView

from teacher.models import Teacher


class TeacherView(View):

    def get(self, request):
        page = request.GET.get('page','')
        teachers = Teacher.objects.all().order_by('-id')
        paginator = Paginator(teachers, 4)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj
        }
        return render(request, 'teacher/teachers_page.html', context)
class TeacherDetailView(TemplateView):
    template_name = 'teacher/teacher_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_id = self.kwargs.get('teacher_id')
        context['teacher'] = Teacher.objects.filter(id=teacher_id).first()
        return context
