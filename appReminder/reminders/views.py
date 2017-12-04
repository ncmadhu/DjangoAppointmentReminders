# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import render

from .models import Appointment

# Create your views here.

class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """ Helps a form a create a new appointment """

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully created'

class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    """ Helps a form to edit existing appointments """

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully updated'

class AppointmentDeleteView(DeleteView):
    """ Helps a user to delete appointment """

    model =  Appointment
    success_url = reverse_lazy('list_appointments')

class AppointmentListView(ListView):
    """ Helps users to list apppintments """

    model =  Appointment

class AppointmentDetailView(DetailView):
    """ Helps users to show detail view of appointment """

    model = Appointment
