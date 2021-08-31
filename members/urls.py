from django.urls import path, include
from .views import UserRegisterView, UserEditView, PasswordChangeView,UserProfile
from .views import PasswordChangeDoneView,ChangeNicknameView,ChangeEmailView,DeleteAccountView,CustomLoginView,CustomLogoutView
from .views import UserRegisterView,ActivationView
from django.contrib.auth import views as auth_views
from . import views
from functions.decorators import staff_only,if_logined_denied,login_only






urlpatterns = [
    path('aktywacja/<str:token>', ActivationView.as_view(), name="activation"),

    path('logowanie/',  CustomLoginView.as_view(),name='login'),
    path('wylogowano/', CustomLogoutView.as_view(),name='logout'),
    path('rejstracja/', if_logined_denied(UserRegisterView.as_view()),name="register"),
    
    path('profil/<str:nickname>/',        login_only(UserProfile.as_view()),name='profile'),
    path('edytuj-profil/',                login_only(UserEditView.as_view()),name='edit-profile'),
    path('zmien-nick/',                   login_only(ChangeNicknameView.as_view()),name='change-nickname'),
    path('zmien-email/',                  login_only(ChangeEmailView.as_view()),name='change-email'),
    path('usun-konto/',                   login_only(DeleteAccountView.as_view()),name='delete-account'),

    path('zmien-haslo/',                  login_only(auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),name='change-password'),
    path('haslo-zmienione/poprawnie/',    login_only(auth_views.PasswordChangeDoneView.as_view(template_name='registration/password-success.html')), name="password_change_done"),
    path('haslo-nie-zostalo-zmienione/',  login_only(views.password_faild), name="password-faild"),

]
