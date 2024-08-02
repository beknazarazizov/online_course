from django.urls import path

from blog.views import BlogsView, BlogDetailTemplateView, add_comment

urlpatterns = [
    path('blog_list/', BlogsView.as_view(), name='blog'),
    path('blog_detail/<int:pk>/', BlogDetailTemplateView.as_view(), name='blog_detail'),
    path('add_comment/<slug:slug>/',add_comment, name='add_comment'),
]