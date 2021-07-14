from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView

from messenger.services import create_new_user, new_user_auto_loging, get_sender_receiver_previous_messages,\
    create_message
from .forms import RegistrationForm, LoginForm, SendMessageForm


class UserListView(ListView):
    model = User
    template_name = 'messenger/user_list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(username=self.request.user.username)


class RegistrationView(View):

    def get(self, request):
        registration_form = RegistrationForm()
        context = {'registration_form': registration_form}
        return render(request, 'messenger/registration_form.html', context)

    def post(self, request):
        reg_form = RegistrationForm(request.POST)
        if request.method == 'POST' and reg_form.is_valid():
            user = create_new_user(reg_form)
            new_user_auto_loging(reg_form, request)
            return redirect('user_list')
        else:
            context = {'registration_form':reg_form, 'method': request.method, 'valid_form': reg_form.is_valid()}
            return render(request, 'messenger/bad_request.html', context)


class LoginView(View):
    form=LoginForm()
    def get(self, request):
        context = {'form':self.form}
        return render(request, 'messenger/login_form.html', context)
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # correct username and password login the user
                login(request, user)
                return redirect('user_list')
            else:
                context = {'form': self.form}
                return render(request, 'messenger/wrong_login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class SendMessageView(TemplateView):
    template_name = 'messenger/message_list.html'
    def get_context_data(self, **kwargs):
        context = {}
        context['message_form'] = SendMessageForm()
        context['sender'], context['receiver'], context['previos_messages'] =\
            get_sender_receiver_previous_messages(self.request, kwargs['user'])
        return context

    def post(self, request, user):
        message_form = SendMessageForm(request.POST)
        create_message(request, message_form, user)
        return redirect('send_message', user)
