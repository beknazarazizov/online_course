from django.urls import path, include

from teacher.views import TeacherView,TeacherDetailView

urlpatterns = [
    path('techers/',TeacherView.as_view(),name='teachers'),
    path('teacher_detail/<int:teacher_id>',TeacherDetailView.as_view(),name='teacher_detail'),
]