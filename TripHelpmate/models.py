import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from MyProject1 import settings


# Create your models here.


class Airports(models.Model):
    name = models.CharField(max_length=100, unique=True)
    continent = models.CharField(max_length=2)
    iso_country = models.CharField(max_length=2)
    country = models.CharField(max_length=100, unique=False)
    city = models.CharField(max_length=100, unique=False)
    icao_code = models.CharField(max_length=4)
    iata_code = models.CharField(max_length=3)
    coordinates = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s, %s" % (self.city, self.country)


class ToDoList(models.Model):
    activity = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.activity


class Item(models.Model):
    name = models.CharField(max_length=256, verbose_name="Item name")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trip(models.Model):
    origin = models.ForeignKey(
        Airports, on_delete=models.CASCADE, related_name="origin"
    )
    destination = models.ForeignKey(
        Airports, on_delete=models.CASCADE, related_name="destination"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, through="ItemTrip", related_name="item")
    activity = models.ManyToManyField(
        ToDoList, through="PlanTrip", related_name="todolist"
    )

    def __str__(self):
        return "from %s to %s" % (self.origin, self.destination)


class ItemTrip(models.Model):
    quantity = models.IntegerField(
        default=1, validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    packed = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default_img.jpg", upload_to="profile_imgs")

    def __str__(self):
        return f"{self.user.username} profile"

    def create_profile(sender, **kwargs):
        if kwargs["created"]:
            user_profile = UserProfile.objects.create(user=kwargs["instance"])

    post_save.connect(create_profile, sender=User)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)


class PlanTrip(models.Model):
    date = models.DateField()
    time = models.TimeField()
    done = models.BooleanField(default=False)
    activity = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


def get_upload_dir(instance, filename):
    return "user_pics/%s/%s/" % (instance.user.username, filename)


class ImgGallery(models.Model):
    picture = models.ImageField(upload_to=get_upload_dir)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
