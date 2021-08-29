from django.db import models
from django.contrib import admin
import uuid
from django.utils.text import slugify
import qrcode
from django.conf import settings
from PIL import Image
import PIL
from os import path
from Customer.models import Client
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

from django.db import connection
# token generation
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

# Model for the clients locations/departments/regions/etc..

class Department(models.Model):
    name = models.CharField(max_length=200)
    # id = models.CharField(primary_key=True, unique=True,
    #                      max_length=200, default="1")
    # print(id)
    creationDate = models.DateField(
        auto_now_add=True, null=True)
    numberOfEntities = models.IntegerField(default=0, editable=False)
    logo = models.CharField(max_length=200, blank=True)


    def save(self, *args, **kwargs):
        # Need to check if it already has an id since we use this method when creating entities
        # otherwise duplicates are created
        # no need to create uuid for anything other than ticket, uuid makes default API functions not work
        # if not len(self.id) == 36:
        #    self.id = str(uuid.uuid4())
        super(Department, self).save()

    def __str__(self):
        text = self.name
        return text




# Making sure that the amount of objects won't exceed the subscription model

def validate_subscription_limit(obj):
    model = obj.__class__
    if(model.objects.count() + obj.quantity > int(connection.get_tenant().subscription) or obj.quantity > int(connection.get_tenant().subscription)):
        raise ValidationError("Can only create " + connection.get_tenant().subscription + " entities. Please contact IISY to upgrade subscription")


class EntityType(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        text = self.name
        return text


# Model for the objects we create a QR code for, ex: computer, garbage bin, projector...


class Entity(models.Model):
    uuid = models.CharField(unique=True,
                            max_length=200, default="1")
    
    entityType = models.ForeignKey(EntityType, on_delete=models.CASCADE, blank=True)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, editable=True, null=True)
    lastTicket = models.DateTimeField(editable=False, null=True)
    slug = models.CharField(max_length=200, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, default="1")
    scanned = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    numberOfOngoingTickets = models.IntegerField(default=0)
    hoursBetweenTickets = models.IntegerField(default=1)
    shouldHaveTextBox = models.BooleanField(default=False)
    #textBoxContent = models.CharField(max_length=200, null=True)
    shouldHaveInfoBox = models.BooleanField(default=False)
    infoBoxContent = models.CharField(max_length=200, blank=True)

    def clean(self):
        validate_subscription_limit(self)

    def save(self, *args, **kwargs):
        # Need to check if it already has an id since we use this method when creating entities
        # Otherwise duplicates are created
        if not len(self.uuid) == 36:
            self.name = self.name
            self.uuid = str(uuid.uuid4())
            self.slug = ('http://' + str(connection.get_tenant().prefix) +
                         '.newdomain.live/' + self.uuid)
            print(str(self.slug))
            self.department.numberOfEntities += 1            
        # Maybe look for a cleaner way to create multiple entities through a form
        # This save methood is pretty crowded
        if self.email =="":
            print('No email found')
            self.email = self.entityType.email        
        for i in range(self.quantity-1):
            current_entity = Entity()
            current_entity.name = self.name
            current_entity.entityType = self.entityType
            current_entity.department = self.department
            current_entity.hoursBetweenTickets = self.hoursBetweenTickets
            current_entity.shouldHaveInfoBox = self.shouldHaveInfoBox
            current_entity.infoBoxContent = self.infoBoxContent
            current_entity.shouldHaveTextBox = self.shouldHaveTextBox
            current_entity.email = self.email
            current_entity.quantity = 0
            current_entity.department.save()
            current_entity.save(current_entity)      
        self.department.save()
        self.quantity = 0
        super(Entity, self).save()


  
    def __str__(self):
        text = self.name
        return text




class Room(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    types = models.ManyToManyField(EntityType)
    uuid = models.CharField(unique=True,
                            max_length=200, default="1",)
    slug = models.CharField(max_length=200, null=True)
    lastTicket = models.DateTimeField(editable=False, null=True)
    hoursBetweenTickets = models.IntegerField(default=1)

    department = models.ForeignKey(Department, on_delete=models.CASCADE )

    def save(self, *args, **kwargs):
        if not len(self.uuid) == 36:
            self.uuid = str(uuid.uuid4())
            self.slug = ('http://' + str(connection.get_tenant().prefix) +
                        '.newdomain.live/' + self.uuid)
            print(str(self.slug))
        super(Room, self).save()

      
    def __str__(self):
        text = self.name
        return text




class Ticket(models.Model):
    MY_CHOICES = (
        ('1', 'Unresolved'),
        ('2', 'Ongoing'),
        ('3', 'Dismissed'),
        ('4', 'Done')
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null = True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null= True)
    type = models.CharField(max_length=200, null=True)
    isRoom = models.BooleanField(default=False)
    location = models.CharField(max_length=200, default="1")
    created = models.DateTimeField(
        auto_now_add=True, editable=True, null=True)
    status = models.CharField(
        max_length=10, choices=MY_CHOICES, default=MY_CHOICES[0][0])
    message = models.CharField(max_length=400)

    def save(self, *args, **kwargs):
        if self.isRoom:
            self.department = self.room.department
            self.location = self.room.location + ' QR code: ' + str(self.room.id)
        else:
            self.entity.numberOfOngoingTickets += 1
            self.location = self.entity.location + ' QR code: ' + str(self.entity.id)
            self.department = self.entity.department
            if self.status == self.MY_CHOICES[3][0]:
                self.entity.numberOfOngoingTickets -= 1
            self.entity.save()
            self.entity_name = self.entity.name
        super(Ticket, self).save()


# for API tokens
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
