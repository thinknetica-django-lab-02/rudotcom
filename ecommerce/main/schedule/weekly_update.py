from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from main.models import Item, Subscriber


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=weekly_update, id='weekly_update', trigger='cron', day_of_week='tue')
    scheduler.start()


def weekly_update():
    last_update = datetime.datetime.now() - datetime.timedelta(days=7)
    # Instances of Item class created since last update
    items = Item.objects.filter(date_added__gte=last_update)
    email_set = {subscriber.user.email for subscriber in Subscriber.objects.get(pk=1).user.all()}
    subject = 'Новый товар!'
    context = {
        "items": items,
    }
    html_message = render_to_string('account/email/weekly_update.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'Marketplace<noreply@marketplace.cc>', email_set, html_message=html_message)
