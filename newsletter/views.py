from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from newsletter.models import MessageVerification, SendNewsletter
from newsletter.forms import SendNewslatterForm
import random
import string
from django.views.generic import CreateView
from myapps.settings import EMAIL_HOST_USER, NOREPLY_EMAIL
from django.core import mail


# Create your views here.
def newsletter_confirmation(request, token):
    if request.method == "GET":
        # take token from request
        path = request.path.split("/")
        token = path[3]

        if MessageVerification.objects.filter(status=False, token=token):
            MessageVerification.objects.filter(token=token).update(status=True)
            # MessageVerification.objects.get(token=None)
            # render succes view

            return render(request, 'newsletter_success.html', {})
        else:
            return render(request, 'newslatter_fail.html', {})


def newsletter_info(request):
    if request.method == "POST":

        # make token
        token = token_maker()

        # user email adress and message
        newslatter_email = request.POST.get(key="newslatter_email")

        domain = get_current_site(request).domain

        link = reverse('newsletter_confirmation', kwargs={
            'token': token
        })

        verification_url = 'http://'+domain+link

        # verification emeil message
        verification_title = "Potwierdzenie adresu email"
        verification_footer = "Jeżeli nie."
        verification_message = f"Here is your verification link: {verification_url}"

        # set data into database for 5 minutes

        # emeil preparation
        email = EmailMessage(
            verification_title,
            verification_message,
            NOREPLY_EMAIL,
            [newslatter_email, ],
        )

       
        if email.send(fail_silently=True,):
          
            if MessageVerification.objects.filter(email=newslatter_email).exists():
           
                if MessageVerification.objects.filter(email=newslatter_email, status=True).exists():
                    
                    return render(request, 'newsletter_info_fail.html', {})
                else:
                    
                    MessageVerification.objects.filter(email=newslatter_email).update(token=token)
                    return render(request, 'newsletter_info.html', {})
            else:
                MessageVerification(email=newslatter_email,token=token).save()
                return render(request, 'newsletter_info.html', {})


class SendNewsletter(CreateView):
    model = SendNewsletter
    template_name = 'send_newsletter.html'
    form_class = SendNewslatterForm

    def post(self, request):
        if request.POST:
            # colecting the data
            subject = request.POST['subject']
            message = request.POST['message']
            current_subscribers = get_current_subscribers()
            my_email = EMAIL_HOST_USER

            # send test emeil only to your self
            if request.POST.get("test_mail"):
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=my_email,
                    recipient_list=my_email,
                    fail_silently=True,
                    html_message=message,
                )
            # send emeil to all subscribers
            else:
                for email in current_subscribers:
                    print(type(email))
                    send_mail(
                        subject=subject,
                        from_email=my_email,
                        message=message,
                        recipient_list=[email, ],
                        fail_silently=True,
                        html_message=message,
                    )
            is_test = request.POST.get("test_mail")
            return render(request, 'sended_info_newsletter.html', {'is_test': is_test})


def token_maker():
    lower_letters = string.ascii_lowercase
    digits = string.digits
    all_strings = lower_letters + digits
    token = "".join(random.choice(all_strings) for units in range(25))
    return token


def send_email(subject, message, email_from, email_to):
    send_mail(
        subject=subject,
        message=message,
        from_email=email_from,
        recipient_list=[email_to],
        fail_silently=True
    )


def get_current_subscribers():
    current_subscribers = []
    for email in MessageVerification.objects.filter(status=True,):
        current_subscribers.append(
            email.email
        )
    return current_subscribers
