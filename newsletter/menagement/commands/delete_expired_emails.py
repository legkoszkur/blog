from django.core.management.base import BaseCommand
from myapps.models import MessageVerification
from datetime import datetime,timedelta


# to będzie można zrealocować dopiero po podłączeniu do servera
# https://cyberfolks.pl/pomoc/jak-ustawic-zadania-cron/
# https://stackoverflow.com/questions/45754860/how-to-auto-delete-the-expires-data-in-the-database
class Command(BaseCommand):
    help = 'Usuwa adresy email nie potwierdzone w ciągu 48h'

    def handle(self, *args,**kwargs):
        now = datetime.now()
        two_days = timedelta(days=2)
        expired = now - two_days
        MessageVerification.objects.filter(state=False,time__lte=expired).delete()
     
