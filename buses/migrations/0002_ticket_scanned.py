# Generated by Django 4.0.2 on 2022-03-21 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='scanned',
            field=models.BooleanField(default=False, help_text='Designates whether a Ticket has already been scanned'),
        ),
    ]
