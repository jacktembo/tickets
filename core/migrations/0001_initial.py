# Generated by Django 4.0.4 on 2022-04-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KazangSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_uuid', models.CharField(max_length=255)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]