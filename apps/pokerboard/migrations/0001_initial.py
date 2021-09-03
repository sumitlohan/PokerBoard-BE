# Generated by Django 2.2 on 2021-09-03 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pokerboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='Name of Pokerboard', max_length=20, unique=True)),
                ('description', models.CharField(help_text='Description', max_length=100)),
                ('estimation_type', models.IntegerField(choices=[(1, 'Series'), (2, 'Even'), (3, 'Odd'), (4, 'Fibonacci')], default=1, help_text='Estimation type')),
                ('duration', models.IntegerField(help_text='Duration for voting (in secs)')),
                ('status', models.IntegerField(choices=[(1, 'Started'), (2, 'Ended')], default=1)),
                ('manager', models.ForeignKey(help_text='Owner of Pokerboard', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket_id', models.SlugField(help_text='Ticket ID imported from JIRA')),
                ('estimate', models.IntegerField(help_text='Final estimate of ticket', null=True)),
                ('rank', models.PositiveSmallIntegerField(help_text='Rank of ticket')),
                ('pokerboard', models.ForeignKey(help_text='Pokerboard to which ticket belongs', on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='pokerboard.Pokerboard')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
