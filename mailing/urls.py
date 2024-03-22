
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import HomePageView, ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, LogsListView

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(HomePageView.as_view()), name='home'),

    path('my_clients/', ClientListView.as_view(), name='client_list'),
    path('my_clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('my_clients/detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('my_clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('my_clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('my_mailing/', MailingListView.as_view(), name='mailing_list'),
    path('my_mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('my_mailing/detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('my_mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('my_mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('my_messages/', MessageListView.as_view(), name='message_list'),
    path('my_messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('my_messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('my_messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('my_logs/', LogsListView.as_view(), name='logs_list'),
]
