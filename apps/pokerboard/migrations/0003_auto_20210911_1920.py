# Generated by Django 2.2 on 2021-09-11 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokerboard', '0002_gamesession_vote'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set(),
        ),
    ]