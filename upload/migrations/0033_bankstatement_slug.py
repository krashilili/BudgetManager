# Generated by Django 2.0.6 on 2018-10-24 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0032_remove_bankstatement_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankstatement',
            name='slug',
            field=models.CharField(blank=True, max_length=63),
        ),
    ]