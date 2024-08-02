import json
import os

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from course.models import Course
from config.settings import BASE_DIR


@receiver(post_save, sender=Course)
def course_post_save(sender, instance,created, **kwargs):
    if created:
        print(f"{instance.titel} created!")

    else:
        print(f"{instance.titel} updated!")


@receiver(pre_delete, sender=Course)
def course_delete(sender, instance, **kwargs):
    directory = 'course/signal_deleted_courses/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(BASE_DIR/directory,'course_{instance.id}.json')


    course_data = {
        'id': instance.id,
        'title': instance.titel,
        'price': instance.price,
        'description': instance.description,
        'teacher': instance.teacher,
        'category': instance.category
    }

    with open(file_path, mode='w') as file_json:
        json.dump(course_data, file_json, indent=4)

    print(f'{instance.titel} is deleted')