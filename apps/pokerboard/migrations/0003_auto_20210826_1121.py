# Generated by Django 2.2 on 2021-08-26 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokerboard', '0002_auto_20210826_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokerboard',
            name='status',
            field=models.CharField(choices=[('STARTED', 'Started'), ('ENDED', 'Ended')], default='STARTED', max_length=20),
        ),
    ]