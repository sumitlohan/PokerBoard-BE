# Generated by Django 2.2 on 2021-09-02 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('group', '0001_initial'),
        ('pokerboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invitee', models.EmailField(help_text='Person invited', max_length=254, null=True)),
                ('group_name', models.CharField(help_text='Name of group', max_length=20, null=True)),
                ('role', models.CharField(choices=[('SPECTATOR', 'Spectator'), ('CONTRIBUTOR', 'Contributor'), ('GUEST', 'Guest')], help_text='Role', max_length=20)),
                ('is_accepted', models.BooleanField(default=False, help_text='Accepted or not?')),
                ('group', models.ForeignKey(help_text='Name of group through which invited, if invited via group', null=True, on_delete=django.db.models.deletion.CASCADE, to='group.Group')),
                ('pokerboard', models.ForeignKey(help_text='Pokerboard', on_delete=django.db.models.deletion.CASCADE, to='pokerboard.Pokerboard')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]