import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from services import send_new_password
from users.forms import UserRegisterForm, UserForm, UserAdminForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:verify_code')
    template_name = 'users/register.html'

    # def get_object(self, queryset=None):
    # """Если пользователь с таким email уже существует"""
    #     email = self.user.email
    #     user = User.objects.filter(email=email).first()
    #     if user:
    #         return redirect('users:login')

    def form_valid(self, form: UserRegisterForm):
        new_user = form.save()
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Код подтверждения {new_user.verify_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return super().form_valid(form)


class VerifyCodeView(View):
    model = User
    template_name = 'users/verify_code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        verify_code = request.POST.get('verify_code')
        user = User.objects.filter(verify_code=verify_code).first()
        if user:
            user.is_verified = True
            user.save()
            return redirect('users:login')

        return redirect('users:verify_code')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile_edit')

    def get_form_class(self):
        if self.request.user.is_staff:
            form_class = UserAdminForm
            return form_class
        form_class = UserForm
        return form_class

    def get_object(self, queryset=None):
        """Редактируем текущего пользователя без передачи pk"""
        return self.request.user

    # def get_object(self, pk=None):  HELP!!!
    #     """Если текущий пользователь - персонал, то редактирует выбранного пользователя из списка с передачей пк.
    #     Если не персонал - редактирует свой профиль без передачи пк."""
    #     if self.request.user.is_staff:
    #         user = User.objects.filter(id=pk)
    #         return user
    #
    #     return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User
    form_class = UserAdminForm

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()


@login_required
def get_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('users:login'))


