# Generated by Django 3.0.3 on 2020-07-20 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationforstudent',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Subject'),
        ),
    ]