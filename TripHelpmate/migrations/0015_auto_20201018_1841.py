# Generated by Django 3.1.1 on 2020-10-18 18:41

import TripHelpmate.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TripHelpmate", "0014_auto_20201018_1607"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imggallery",
            name="picture",
            field=models.ImageField(
                default="default_pic.jpg", upload_to=TripHelpmate.models.get_upload_dir
            ),
        ),
    ]
