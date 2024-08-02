from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify

from blog.models import Author, Blog
from course.managers import CustomUserManager
from teacher.models import Teacher


class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories_images', null=True, blank=True)
    @property
    def get_cours_video(self):
        video=Category.objects.filter(courses__video__in=Course.objects.filter(category__title=self.title))
        return video

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number_of_students = models.IntegerField(default=0)
    price = models.FloatField()
    duration = models.IntegerField()
    teachers = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    video = models.FileField(upload_to='media/courses/video' ,null=True,)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def duration_of_video(self):
        if self.duration >= 60:
            hours = self.duration // 60
            minutes = self.duration % 60
            return hours, minutes

    objects = models.Manager
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.slug:
            i = 1
            while True:
                new_slug = f"{slugify(self.title)}-{i}"
                if not Course.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
                i += 1

        super(Course, self).save(*args, **kwargs)
    def __str__(self):
        return self.title


class Comment(models.Model):
    class RatingChoices(models.TextChoices):
        Zero = '0'
        One = '1'
        Two = '2'
        Three = '3'
        Four = '4'
        Five = '5'

    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField()
    is_published = models.BooleanField(default=False)
    rating = models.CharField(max_length=100, choices=RatingChoices.choices, default=RatingChoices.Zero.value)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments')

class UserConfirmationModel(models.Model):
    code = models.IntegerField()
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email} - {self.code}'

    class Meta:
        verbose_name = 'code'
        verbose_name_plural = 'codes'



