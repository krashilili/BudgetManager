# Generated by Django 2.0.6 on 2018-10-21 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0017_auto_20181021_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankstatementdocument',
            name='uploaded_at',
        ),
    ]
