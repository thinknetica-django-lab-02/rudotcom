import os

from django.conf import settings


def get_filename(filename, request):
    return filename.upper()


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.category.slug}_{instance.slug}.{ext}'
    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
    return f'{filename}'


def upload_avatar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.user.username}.{ext}'
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return f'avatar/{filename}'
