from django.contrib import admin

# Register your models here.
from course.models import Course,Comment,Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'number_of_students', 'price','video', 'duration', 'teachers', 'category',]
    list_display = ('title',  'number_of_students', 'price')
    search_fields = ('title', 'teachers')
    list_filter = ('duration', 'price')
# admin.site.register(Course)
admin.site.register(Comment)
# admin.site.register(Category)
