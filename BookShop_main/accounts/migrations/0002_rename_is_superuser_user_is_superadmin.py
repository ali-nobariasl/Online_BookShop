# Generated by Django 4.2.2 on 2023-06-15 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_superuser',
            new_name='is_superadmin',
        ),
    ]
