import os.path
from django.core.mail import send_mail

from config import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import json
import os.path
from teacher.models import Teacher


@receiver(pre_delete, sender=Teacher)
def customers_delete(sender, instance, **kwargs):
    directory = 'teacher/deleted_teacher'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{instance.full_name}_id_{instance.id}')
    data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'joined': str(instance.joined),
        'email': instance.email,
        'image':str(instance.image),

    }

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            print(f"{instance.full_name} deleted successfully")
    except IOError as e:
        raise e


@receiver(post_save, sender=Teacher)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        subject = f'Hi {instance.full_name}'
        message = 'Your account has been added and saved successfully as customer. Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [instance.email]
        try:
            send_mail(subject, message, email_from, email_to)
            print(f'Email sent to {instance.email}')
        except Exception as e:
            print(e)
            raise f'Error sending email: {str(e)}'