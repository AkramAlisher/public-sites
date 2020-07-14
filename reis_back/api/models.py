from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cargo(models.Model):
    location_from = models.CharField(max_length=200)
    location_to = models.CharField(max_length=200)
    date = models.DateField()
    description = models.CharField(max_length=300, default="", blank=True)
    weight = models.CharField(max_length=100)
    volume = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, default="", blank=True)
    contact_person = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="", blank=True)
    phone = models.CharField(max_length=15)
    additional_information = models.CharField(max_length=300, default="", blank=True)
    top = models.BooleanField(default="False")
    top_date = models.DateField(null=True, blank=True)
    top_date_end = models.DateField(null=True, blank=True)
    pin = models.BooleanField(default="False")
    pin_date = models.DateField(null=True, blank=True)
    pin_date_end = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField()
    views = models.IntegerField(default="0")


class Vehicle(models.Model):
    location_from = models.CharField(max_length=200)
    location_to = models.CharField(max_length=200)
    date = models.DateField()
    description = models.CharField(max_length=300, default="")
    capacity = models.CharField(max_length=100, default="")
    volume = models.CharField(max_length=100, default="")
    cost = models.CharField(max_length=100, default="")
    company_name = models.CharField(max_length=100, default="", blank=True)
    contact_person = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="", blank=True)
    phone = models.CharField(max_length=15)
    additional_information = models.CharField(max_length=300, default="", blank=True)
    top = models.BooleanField(default="False")
    top_date = models.DateField(null=True, blank=True)
    top_date_end = models.DateField(null=True, blank=True)
    pin = models.BooleanField(default="False")
    pin_date = models.DateField(null=True, blank=True)
    pin_date_end = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField()
    views = models.IntegerField(default="0")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


