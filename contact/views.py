from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import urllib
from myapps.settings import EMAIL_HOST_USER
import json
from myapps import settings 



def contact_details(request):
    return render(request,'contact_details.html',{})

def contact_info(request):
     if request.method=="POST":

        '''Capcha'''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        data = urllib.parse.urlencode(values).encode("utf-8")
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        result = json.load(response)
        

        '''Captcha end'''
        if result['success']:
            guest_name = request.POST["cname"]
            guest_email = request.POST["cemeil"]
            guest_message = request.POST["cmessage"]
            guest_subject = f"Użytkownik:{guest_name} o adresie {guest_email} przesyła ci wiadomość"
            message_to_emeil = f"{guest_message}"
            subject = f"Masz nową wiadomość od użytkownika: {guest_name}."


            send_mail(
                subject=subject,
                message=guest_message,
                from_email=guest_email,
                recipient_list=[EMAIL_HOST_USER,],
                fail_silently=True
                )

            return render(request, 'contact_success.html', {})
        else:

            return render(request, 'contact_fail.html', {})



