# Generated by Django 2.0.6 on 2018-10-23 21:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0028_auto_20181023_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatementdocument',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 23, 21, 48, 26, 191179), editable=False),
        ),
    ]