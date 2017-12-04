# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from timezone_field import TimeZoneField
from appReminder import celery_app

import arrow

# Create your models here.
class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number =  models.CharField(max_length=15)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='US/Pacific')

    # Hidden Fields
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('view_appointment', args=[str(self.id)])

    
    def clean(self):
        """ Checks appointment are not scheduled in the past """
        appointment_time = arrow.get(self.time, self.time_zone.zone)

        if appointment_time < arrow.utcnow():
            raise ValidationError('Apppointment occurs in the past')

    def schedule_reminder(self):
        """ Schedules a celery task to send a reminder """

        appointment_time = arrow.get(self.time, self.time_zone.zone)
        reminder_time = appointment_time.replace(minutes=-settings.REMINDER_TIME)

        """ schedule a celery task """
        from .tasks import send_sms_reminder
        result = send_sms_reminder.apply_async((self.pk,), eta = reminder_time)

        return result.id

    def save(self, *args, **kwargs):
        """ custom save method which also schedules a reminder """

        if self.task_id:
            # revoke the task if time has changed
            celery_app.control.revoke(self.task_id)

        super(Appointment, self).save(*args, **kwargs)

        self.task_id = self.schedule_reminder()

        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)
