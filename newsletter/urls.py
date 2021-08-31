from django.urls import path
from newsletter.views import newsletter_info, newsletter_confirmation, SendNewsletter
from functions.decorators import superuser_only


urlpatterns = [  
    path('info/',                   superuser_only(newsletter_info) , name="newsletter-info"),
    path('wyslij/',                 superuser_only(SendNewsletter.as_view()),name='send-newsletter'),
    path('potwierdzenie/<token>',   superuser_only(newsletter_confirmation),name='newsletter_confirmation'),
]