from django import forms

from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from smtplib import SMTPException

from mailing.models import Mailing, Logs


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


def change_status(mailing, check_time) -> None:
    if mailing.status == 'created':
        mailing.status = 'started'
        print('started')
    elif mailing.status == 'started' and mailing.date_stop <= check_time:
        mailing.status = 'completed'
        print('completed')
    mailing.save()


def change_date_start(mailing, check_time):
    if mailing.date_start < check_time:
        if mailing.period == 'daily':
            mailing.date_start += timedelta(days=1)
        elif mailing.period == 'weekly':
            mailing.date_start += timedelta(days=7)
        elif mailing.period == 'monthly':
            mailing.date_start += timedelta(days=30)
    mailing.save()


def automatic_mailing():
    print('automatic_mailing работает')
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    mailings = Mailing.objects.filter(is_active='True')
    if mailings:
        for mailing in mailings:
            if mailing.date_start <= now <= mailing.date_stop:
                change_status(mailing, now)
                for client in mailing.client.all():
                    try:
                        response = send_mail(
                            subject=mailing.message.title,
                            message=mailing.message.text_body,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.email],
                            fail_silently=False,
                        )
                        mailing_log = Logs.objects.create(
                            attempt_time=mailing.date_start,
                            attempt_status=True,
                            server_response=response,
                            mailing=mailing,
                            client=client,
                        )
                        mailing_log.save()
                        change_date_start(mailing, now)
                        print('mailing_log сохранён')
                    except SMTPException as error:
                        mailing_log = Logs.objects.create(
                            attempt_time=mailing.date_start,
                            attempt_status=False,
                            server_response=error,
                            mailing=mailing,
                            client=client,
                        )
                        mailing_log.save()
                        print(error)
    else:
        print('no mailings')




def my_job_draft():
    now = datetime.now()
    print(f'Now {now} - yeeeeees !!!')
