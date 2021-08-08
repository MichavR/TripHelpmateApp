# Generated by Django 3.1.1 on 2020-10-15 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("TripHelpmate", "0010_auto_20201015_1401"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemtrip",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="itemtrip",
                to="TripHelpmate.trip",
            ),
        ),
        migrations.AlterField(
            model_name="plantrip",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plantrip",
                to="TripHelpmate.trip",
            ),
        ),
    ]
