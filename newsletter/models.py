from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from ckeditor.fields import RichTextField



class MessageVerification(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=25)
    time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        #expiration = self.time + timedelta(
        #    days=2
        #)
        output = f"POTWIERDZONY: {self.status} / EMAIL: {self.email} / DATE: {self.time} ID:{self.id} / TOKEN:{self.token}"
        return output

class SendNewsletter(models.Model):
    test_mail = models.BooleanField(default=True,)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(max_length=200)
    message = RichTextField()

    def __str__(self):
        output = f"TEST MAIL:{self.test_mail} / DATA:{self.date} / TEMAT: {self.subject}"
        return output


