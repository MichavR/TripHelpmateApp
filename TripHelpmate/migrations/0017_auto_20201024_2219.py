# Generated by Django 3.1.1 on 2020-10-24 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TripHelpmate', '0016_auto_20201019_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Item name'),
        ),
    ]