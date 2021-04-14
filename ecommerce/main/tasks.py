# Create your tasks here

from celery import shared_task

from main.models import Vendor


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Vendor.objects.count()


@shared_task
def rename_vendor(vendor_id, name):
    w = Vendor.objects.get(id=vendor_id)
    w.name = name
    w.save()
