from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, LoginView, \
    PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView

from users.forms import CustomUserChangeForm, CustomUserRegisterForm, CustomAuthenticationForm, CustomPasswordResetForm, \
    CustomResetConfirmForm
from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('catalog_app:product_list')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = CustomUserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        subject = 'Верификация учетной записи'
        message = f'Здравствуйте {user.first_name}, пожалуйста проверьте свою учетную запись, перейдя по этой ссылке: ' \
                  f'http://localhost:8000{reverse_lazy("users:verify_account", kwargs={"user_pk": user.pk})}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return response


def verify_account(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect(to=reverse('users:login'))


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog_app:product_list')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/email_reset.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomResetConfirmForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
