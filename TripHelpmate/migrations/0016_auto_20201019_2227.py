# Generated by Django 3.1.1 on 2020-10-19 22:27

import TripHelpmate.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TripHelpmate", "0015_auto_20201018_1841"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imggallery",
            name="picture",
            field=models.ImageField(upload_to=TripHelpmate.models.get_upload_dir),
        ),
    ]
