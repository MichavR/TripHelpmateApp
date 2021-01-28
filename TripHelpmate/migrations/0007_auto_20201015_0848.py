# Generated by Django 3.1.1 on 2020-10-15 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TripHelpmate', '0006_todolist_trip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='done',
        ),
        migrations.RemoveField(
            model_name='todolist',
            name='trip',
        ),
        migrations.CreateModel(
            name='PlanTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TripHelpmate.todolist')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TripHelpmate.trip')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='activity',
            field=models.ManyToManyField(related_name='trip_activity', through='TripHelpmate.PlanTrip', to='TripHelpmate.ToDoList'),
        ),
    ]