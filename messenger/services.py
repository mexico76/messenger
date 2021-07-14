from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q

from messenger.models import Messages


def create_new_user(reg_form):
    user = User.objects.create_user(username=reg_form.cleaned_data.get('user_login'),
                                    email=reg_form.cleaned_data.get('user_email'),
                                    password=reg_form.cleaned_data.get('user_password'),
                                    first_name=reg_form.cleaned_data.get('user_name'),
                                    last_name=reg_form.cleaned_data.get('user_surname'), )
    return user

def new_user_auto_loging(reg_form, request):
    new_user = authenticate(username=reg_form.cleaned_data['user_login'],
                            password=reg_form.cleaned_data['user_password'],
                            )
    if new_user is not None:
        sing_in = login(request, new_user)
        return sing_in
    else:return 'there is no user'


def get_sender_receiver_previous_messages(request, user):
    sender = User.objects.get(username=request.user)
    receiver = User.objects.get(username=user)
    previos_messages = Messages.objects.filter(Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver)
                                                   & Q(receiver=sender)).order_by('-date_time')
    return sender, receiver, previos_messages


def create_message(request, message_form, user):
    if message_form.is_valid() and request.method == 'POST':
        create_message = Messages.objects.create(sender=request.user, receiver=User.objects.get(username=user),
                                                 message_text=message_form.cleaned_data.get('message_text'))
        create_message.save()