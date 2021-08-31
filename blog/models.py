from django.db import DefaultConnectionProxy, models
from members.models import CustomUser
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.contrib import admin
from django.utils import timezone
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    slug = models.SlugField(max_length=70)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

class Post(models.Model):
    class Meta:
        db_table = "article"

    title = models.CharField(max_length=255)  
    title_tag = models.CharField(blank=False, max_length=255, default=" ")
    header_image = models.ImageField(upload_to="images/article_head/", default="images/article_head/default.jpg")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50,)
    snippet = models.CharField(max_length=350,default='') 
    published = models.BooleanField(default=False,)
    text_to_url = models.CharField(max_length=300,default=" ",unique=True,null=False,blank=False,)
    slug = models.SlugField(max_length=30,default=uuid.uuid4, editable=False, unique=True)
   
    
    def __str__(self):
        return self.title + '|  ' + '  |' + str(self.post_date)

    def get_absolute_url(self):
        return reverse('article-view', args=[str(self.text_to_url)])


class ArticleStatistic(models.Model):
    class Meta:
        db_table = "ArticleStatistic"
    
    article = models.ForeignKey(Post,on_delete=models.CASCADE)                    
    date = models.DateField('Date', default=timezone.now)   
    views = models.IntegerField('Views', default=0)     
    
    def __str__(self):
        return self.article.title
      
class ArticleStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'views')  
    search_fields = ('__str__', )      

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    # teraz kminie sprawę z foregin key
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE) 
    body = models.TextField(max_length=3000)  
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    reponse_to = models.CharField(max_length=40,blank=True,null=True)
    reponse_to_id = models.IntegerField(blank=True,null=True,default=0)
    slug = models.SlugField(max_length=30,default=uuid.uuid4, editable=False, unique=True)
    

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        output = f"COMMENT_ID:{self.id} / RESPONSE_TO:{self.reponse_to_id} / POST_ID:{self.post.id} / NAME: {self.user} / DATE: {self.date}"
        return output

    def children(self):
        return Comment.objects.filter(parent=self).order_by('date')

    def reply_amount(self):
        return Comment.objects.filter(parent=self).count()

class CommentReports(models.Model):
    who_report = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    report_body = models.TextField(max_length=100,null=False,blank=False)
    reported_comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    uuid = models.UUIDField(max_length=30,default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        output = f"{self.id} / {self.uuid}  WHO REPORTED: {self.who_report} / REPORETD COMMENT ID: {self.reported_comment.id}"
        return output
    



  

    

    

    
    



    




