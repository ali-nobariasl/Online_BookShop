# Generated by Django 4.2.2 on 2023-07-11 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(blank=True, max_length=150, null=True),
        ),
    ]
