# Generated by Django 3.1.1 on 2020-10-10 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("TripHelpmate", "0002_auto_20201009_1958"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="ItemTrip",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("packed", models.BooleanField(default=False)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TripHelpmate.item",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="trip",
            name="luggage",
        ),
        migrations.AlterField(
            model_name="todolist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="auth.user"
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="auth.user"
            ),
        ),
        migrations.DeleteModel(
            name="Luggage",
        ),
        migrations.AddField(
            model_name="itemtrip",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="TripHelpmate.trip"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="trip",
            field=models.ManyToManyField(
                related_name="trip",
                through="TripHelpmate.ItemTrip",
                to="TripHelpmate.Trip",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="item",
            field=models.ManyToManyField(
                related_name="item",
                through="TripHelpmate.ItemTrip",
                to="TripHelpmate.Item",
            ),
        ),
    ]
