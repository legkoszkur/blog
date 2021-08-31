from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth.forms import  PasswordChangeForm
from members.forms import CustomUserChangeForm,CustomUserCreationForm
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from .forms import PasswordChangingForm,EditCustomUserForm,NicknameChangeForm,EmailChangeForm
from django.views.generic import DetailView
from members.models import CustomUser,ActivationLinks
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from myapps.settings import EMAIL_HOST_USER
from functions.functions import token_maker
from django.contrib.sites.shortcuts import get_current_site



from django.contrib.auth.views import LoginView,LogoutView

class CustomLoginView(LoginView):
    model = CustomUser
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

class UserProfile(DetailView):
    model = CustomUser
    template_name = 'registration/profile.html'

    def get(self,request,*args,**kwargs):

        user = get_object_or_404(CustomUser, nickname=self.kwargs['nickname'])

        context = {
            'current_user':user,
            }

        return render(request, template_name=self.template_name, context=context)

class UserEditView(generic.UpdateView):
    form_class = EditCustomUserForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class UserRegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get(self,request,*args,**kwargs):
        form = self.form_class
        return render(request,template_name=self.template_name, context={"form": form})

    def post(self,request,*args,**kwargs):
        form = CustomUserCreationForm(request.POST)
        print(100*"0")
        guest_email = request.POST['email']
        print(100*"1")
        user_data = form.save()
        print(100*"2")
        
        user_id = CustomUser.objects.filter(email=guest_email).get().id
        token = ActivationLinks.objects.filter(user=user_id).get().token

        domain = get_current_site(request).domain
        link = reverse('activation',kwargs={
                        'token':token
                        })
        verification_url = 'http://'+domain+link


        subject = "Aktywacja konta w serwisie legkoszkur.com"
        guest_message = f"Witaj, bardzo mi miło że dokonałeś rejstracji na moim blogu. Od tej pory gdy tylko potwierdzisz restracje będziesz mógł logować się do serwisu oraz dodawać komentarze pod postami. Kilknij na poniższy link aby dokończyć proces restracji:{verification_url}"
        

        send_mail(
                subject=subject,
                message=guest_message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[guest_email,],
                fail_silently=True
                )

        return render(request,'registration/register_info.html',{})

class ActivationView(generic.UpdateView):
    model = ActivationLinks

    def get(self,request,*args,**kwargs):
        path = request.path.split("/")
        token = path[3]

        if ActivationLinks.objects.filter(token=token):

            user_id = ActivationLinks.objects.filter(token=token).get().id
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()
            
            token = ActivationLinks.objects.get(token=token)
            token.token = None
            token.save()

            return render(request,'registration/email_confirmation_success.html',{})
        else:
            return render(request,'registration/email_confirmation_fail.html',{})

def password_success(request):
    return render(request,'registration/password-success.html',{})

def password_faild(request):
    return render(request,'registration/password-faild.html',{})

class ChangeNicknameView(generic.UpdateView):
    form_class = NicknameChangeForm
    template_name = 'registration/change_nickname.html'


    def get_object(self):
        return self.request.user

    def post(self,request,*args,**kwargs):
        current_user_id = self.request.user.id
        new_nickname = request.POST['nickname']
        try:
            CustomUser.objects.filter(id = current_user_id).update(nickname=new_nickname)
        except IntegrityError as err:
            error_contents = "Niestety ten nick jest już zajęty."
            context = {
                'form':self.form_class,
                'error': error_contents,
            }

            return render(request, template_name=self.template_name, context=context)
        else:
            return redirect(reverse('edit-profile'))

class ChangeEmailView(generic.UpdateView):
    form_class = EmailChangeForm
    template_name = 'registration/change_email.html'

    def get_object(self):
        return self.request.user

    def post(self,request,*args,**kwargs):
        current_user_id = self.request.user.id
        new_email = request.POST['email']
        try:
            CustomUser.objects.filter(id = current_user_id).update(email=new_email)
        except IntegrityError as err:
            error_contents = "Niestety ten email jest już zajęty."
            context = {
                'form':self.form_class,
                'error': error_contents,
            }

            return render(request, template_name=self.template_name, context=context)
        else:
            return redirect(reverse('edit-profile'))

class DeleteAccountView(DetailView):
    model = UserProfile
    template_name = 'registration/delete_user.html'

    def get_object(self):
        return self.request.user

    def post(self,request,*args,**kwargs):
        current_user = self.request.user
        result1 = current_user.check_password(request.POST['password1'])
        result2 = current_user.check_password(request.POST['password2'])
        context={

        }

        if result1 and result2:

            self.request.user.delete()
            return redirect(reverse('login'))
        else:
            context['error'] = "Nie prawidłowe dane."
            return render(request, template_name=self.template_name, context=context)
        
              
       



