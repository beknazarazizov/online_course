from django.db import models
from django.utils.text import slugify



class Teacher(models.Model):
    class LevelChoices(models.TextChoices):
        JUNIOR = 'Junior','JUNIOR'
        MIDDLE = 'MIDDLE','Middle'
        SINIOR = 'SINIOR','Sinior'
        OTHER = 'OTHER','Other'


    full_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    rating = models.CharField(choices=LevelChoices.choices,default=LevelChoices.OTHER.value)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    additional_work = models.CharField(default='Teacher of University')
    twitter_link = models.CharField(max_length=150, null=True, blank=True)
    facebook_link = models.CharField(max_length=150, null=True, blank=True)
    linkedin_link = models.CharField(max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)

        if self.slug:
            i = 1
            while True:
                new_slug = f"{slugify(self.full_name)}-{i}"
                if not Teacher.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
                i += 1

        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

