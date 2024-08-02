from django.contrib import admin
from django.urls import path, include

import course
from course.views.auth import logout_page, RegisterView, verify_email_done, LoginPageView, SendEmailView, confirmation_view
from course.views.views import IndexPageView, AboutPage, ContactPage, CategoryView, CoursePage, CourseDetailView,send_email

urlpatterns = [
    path('home/',IndexPageView.as_view(),name='home'),
    path('category/', CategoryView.as_view(), name='category'),
    path('about/',AboutPage.as_view(),name='about'),
    path('contact/',ContactPage.as_view(),name='contact'),
    path('courses/',CoursePage.as_view(),name='courses'),
    path('course_detail/<int:pk>/',CourseDetailView.as_view(),name='course_detail'),
    #authenticate
    path('login-page/', LoginPageView.as_view(), name='login'),
    path('logout-page/',logout_page,name='logout'),
    path('register/',RegisterView.as_view,name='register'),
    # path('export-data/', export_data, name='export_data'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),
    path('activate/<uidb64>/<token>/', course.views.auth.activate, name='activate'),
    path('verify_email_done/',verify_email_done,name='verify_email_done'),
    path('send_messeg/',send_email,name='send_messeg'),
    path('confirm/', confirmation_view, name='confirm'),

]