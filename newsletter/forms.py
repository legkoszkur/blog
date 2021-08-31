
from django import forms
from .models import SendNewsletter


class SendNewslatterForm(forms.ModelForm):
    class Meta:
        model = SendNewsletter
        fields = ('test_mail','subject','message')
        test_mail = forms.BooleanField(initial=True)
        widgets = {
            'subject': forms.Textarea( attrs={
                                            'class':'form-control',
                                            'type':'text'
                                            }
                                    ),

            'message': forms.Textarea( attrs={'class':'form-control'}),
        }
  