from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView

from blog.models import Blog
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Mailing, Message, Logs


class HomePageView(TemplateView):
    """Отображение домашней страницы"""
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['active_mailing_count'] = Mailing.objects.filter(is_active=True,).count()
        context_data['clients_count'] = Client.objects.all().distinct().count()
        context_data['three_posts'] = Blog.objects.all()[:3]

        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            return self.object
        raise Http404


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(attempt_status=True).count()
        context_data['error'] = context_data['object_list'].filter(attempt_status=False).count()
        return context_data


@login_required
def active_toggle(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect(reverse('mailing:mailing_list'))
