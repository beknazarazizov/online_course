from django.contrib import admin

from blog.models import Blog,Author

# Register your models here.
admin.site.register(Author)
admin.site.register(Blog)

