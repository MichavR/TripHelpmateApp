# Generated by Django 3.1.1 on 2020-10-11 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("TripHelpmate", "0003_auto_20201010_1246"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="trip",
        ),
    ]
