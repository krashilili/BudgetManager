# Generated by Django 2.0.6 on 2018-10-24 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0034_auto_20181024_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatement',
            name='slug',
            field=models.SlugField(blank=True, max_length=63),
        ),
    ]
