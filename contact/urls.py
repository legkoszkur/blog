from django.urls import path
from contact.views import contact_details, contact_info


urlpatterns = [
    path('szczegoly/',contact_details, name='contact_details'),
    path('info/',contact_info, name='contact_info'),
]