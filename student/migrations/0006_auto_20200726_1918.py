# Generated by Django 3.0.3 on 2020-07-26 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_notificationforstudent_notyfy_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationforstudent',
            old_name='notyfy_class',
            new_name='notify_class',
        ),
    ]