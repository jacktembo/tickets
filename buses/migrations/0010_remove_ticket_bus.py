# Generated by Django 4.0.2 on 2022-03-08 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0009_alter_ticket_bus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='bus',
        ),
    ]
