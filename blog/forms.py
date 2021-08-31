
from django import forms
from .models import Post, Category,Comment,CommentReports



class PostForm(forms.ModelForm): 
    class Meta:
        model = Post
        author = forms.TextInput() 
        fields = ('published','title','title_tag','author','category','body','snippet','header_image','text_to_url')
        
        widgets = {
            'author': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'login-user',
                    'value':'',
                    'type':'hidden',
                    },),
        }
        
    def __init__(self, *args, **kwargs):
        super(PostForm,self).__init__(*args, **kwargs)
        choices = Category.objects.all().values_list('name','name')
        self.fields['category'] = forms.ChoiceField(choices=choices)       

class EditForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ('published','title','title_tag','category','body','snippet','header_image','text_to_url')

    def __init__(self, *args, **kwargs):
        super(EditForm,self).__init__(*args, **kwargs)
        choices = Category.objects.all().values_list('name','name')
        self.fields['category'] = forms.ChoiceField(choices=choices)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
            
class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = CommentReports
        fields = ('report_body',)

          

