# Generated by Django 4.2.2 on 2023-06-22 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'VENDOR'), (2, 'CUSTOMER')], null=True),
        ),
    ]
