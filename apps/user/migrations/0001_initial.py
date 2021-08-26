# Generated by Django 2.2 on 2021-08-25 12:31

import apps.user.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(help_text='Email Address', max_length=50, unique=True)),
                ('first_name', models.CharField(help_text='First Name of User', max_length=50)),
                ('last_name', models.CharField(help_text='Last Name of User', max_length=50)),
                ('is_staff', models.BooleanField(default=False, help_text='This user can access admin panel')),
                ('is_admin', models.BooleanField(default=False, help_text='This user has all permissions without explicitly assigning them')),
                ('password', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$', message='Password must be of minimum 8 characters, at least one uppercase letter, lowercase letter, number and special character')])),
                ('is_account_verified', models.BooleanField(default=False, help_text='This account has verified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('expired_at', models.DateTimeField(default=apps.user.utils.get_expire_date)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'abstract': False,
            },
        ),
    ]
