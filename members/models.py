from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from functions.functions import token_maker




class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    nickname = models.CharField(unique=True,default="",max_length=100)
    biogram = models.TextField(default="Parę słów o mnie.",max_length=1000)
    job = models.CharField(max_length=30,null=True,default="Nie podano")
    profile_picture = models.ImageField(default="images/profile_pic/default.png",upload_to="images/profile_pic/")
    own_website_url = models.CharField(max_length=255,null=True,default="#")
    linkedin_url = models.CharField(max_length=255,null=True,default="#")
    github_url = models.CharField(max_length=255,null=True,default="#")
    facebook_url = models.CharField(max_length=255,null=True,default="#")
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


    def save(self,*args,**kwargs):
        if not self.nickname:
                user_emaial = self.email
                user_emaial = str(user_emaial)
                first_part_of_email = user_emaial.split('@')[0]
                random_numbers = token_maker(5) 
                self.nickname = str(first_part_of_email) + "%" + str(random_numbers)

        if self.is_superuser:
            self.is_admin = True

        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            ActivationLinks.objects.create(user=self)

        super(CustomUser,self).save(*args,**kwargs)


class ActivationLinks(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    token = models.CharField(max_length=50,null=True,default=token_maker(50),unique=True)




