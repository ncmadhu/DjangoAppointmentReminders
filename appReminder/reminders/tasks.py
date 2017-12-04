from __future__ import absolute_import

import arrow
from celery import shared_task
from django.conf import settings
from twilio.rest import Client

from .models import Appointment

TWILIO_ACCOUNT_SID='AC59ee43346408feaa2a57d1948fece976'
TWILIO_AUTH_TOKEN='9227dd86ea031bf132b57599cd24fe71'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@shared_task
def send_sms_reminder(appointment_id):
    """ Send reminder to phone using Twilio SMS """
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        """ Appointment has been deleted """
        return

    appointment_time = arrow.get(appointment.time, appointment.time_zone.zone)
    body = 'Hi {0}. You have a appointment at {1}'.format(
            appointment.name,
            appointment_time.format('h:mm a')
            )

    message = client.messages.create(
            body=body,
            to=appointment.phone_number,
            from_=settings.TWILIO_NUMBER,
            )
