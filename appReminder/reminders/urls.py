from django.conf.urls import url

from .views import AppointmentCreateView, AppointmentUpdateView, AppointmentDeleteView, AppointmentListView, AppointmentDetailView

urlpatterns = [
        url(r'^new$', AppointmentCreateView.as_view(), name='new_appointment'),
        url(r'^(?P<pk>[0-9]+)/edit$', AppointmentUpdateView.as_view(), name='edit_appointment'),
        url(r'^(?P<pk>[0-9]+)/delete', AppointmentDeleteView.as_view(), name='delete_appointment'),

        url(r'^$', AppointmentListView.as_view(), name='list_appointments'),
        url(r'^(?P<pk>[0-9]+)$', AppointmentDetailView.as_view(), name='view_appointment'),
        ]
