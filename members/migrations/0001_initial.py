# Generated by Django 3.1.6 on 2021-05-16 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('nickname', models.CharField(default='', max_length=100, unique=True)),
                ('biogram', models.TextField(default='Parę słów o mnie.', max_length=1000)),
                ('job', models.CharField(default='Nie podano', max_length=30, null=True)),
                ('profile_picture', models.ImageField(default='images/profile_pic/default.png', upload_to='images/profile_pic/')),
                ('own_website_url', models.CharField(default='#', max_length=255, null=True)),
                ('linkedin_url', models.CharField(default='#', max_length=255, null=True)),
                ('github_url', models.CharField(default='#', max_length=255, null=True)),
                ('facebook_url', models.CharField(default='#', max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivationLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='l935m3dvpfdao2gsdqqgrrd3f8z6bgelhhk7iscwkssu64ti05', max_length=50, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
