# Generated by Django 4.0.2 on 2022-02-25 10:39

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_alter_event_additional_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='additional_information',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
