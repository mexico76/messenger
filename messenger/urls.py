from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import UserListView, LoginView, RegistrationView, LogoutView, SendMessageView

urlpatterns = [
    path('', login_required(UserListView.as_view()), name='user_list'),
    path('login/', LoginView.as_view(),  name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('message_to_<slug:user>/', login_required(SendMessageView.as_view()), name='send_message'),
]