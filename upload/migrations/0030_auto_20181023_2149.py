# Generated by Django 2.0.6 on 2018-10-23 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0029_auto_20181023_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatementdocument',
            name='uploaded_at',
            field=models.DateTimeField(editable=False),
        ),
    ]
