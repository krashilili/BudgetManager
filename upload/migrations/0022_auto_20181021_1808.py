# Generated by Django 2.0.6 on 2018-10-21 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0021_auto_20181021_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankstatementdocument',
            name='bank',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='bankstatementdocument',
            name='owner',
            field=models.CharField(max_length=255),
        ),
    ]
