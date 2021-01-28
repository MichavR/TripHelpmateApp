# Generated by Django 3.1.1 on 2020-10-15 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TripHelpmate', '0005_auto_20201011_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='trip',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='trip_activities', to='TripHelpmate.trip'),
            preserve_default=False,
        ),
    ]