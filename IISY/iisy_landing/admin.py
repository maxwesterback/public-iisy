from django.contrib import admin
from .models import Department
from .models import Entity
from .models import Ticket
from .models import EntityType
from .models import Room

import qrcode
from os import path
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
import PIL
from django.http import HttpResponse
import zipfile
from io import BytesIO


# Inline form for entities displaying tickets
class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ['location', ]

# Inline form for Department displaying entities


class EntityInLine(admin.TabularInline):
    model = Entity
    extra = 0
    exclude = ('quantity',)
    readonly_fields = ['id', 'slug', 'uuid']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'numberOfEntities']
    list_filter = ('name',)
    #inlines = [EntityInLine, ]
    readonly_fields = ['id']

class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

# Action for qr codes


def make_qr_codes(modeladmin, request, queryset):
    buffer = BytesIO()
    zf = zipfile.ZipFile(buffer, 'w')
    i=1
    for obj in queryset:
        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=5
        )
        qr.add_data(obj.slug)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        width, height = img.size
        draw = ImageDraw.Draw(img)
        text_name = obj.name  + str(obj.id)
        draw.text((40, height - 40), text_name)
        temp = tempfile.TemporaryFile()
        img.save(temp)
        temp.seek(0)
        zf.writestr(obj.name + str(obj.id) +  '.png', temp.read())
        i+=1
    zf.close()
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename=qr_codes.zip'
    return response

    

  


make_qr_codes.short_description = "Make qr codes for selected devices"


class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    actions = [make_qr_codes]

    readonly_fields = ['uuid', 'slug']



class EntityAdmin(admin.ModelAdmin):
    list_display = ('entityType', 'name', 'id', 'department', 'numberOfOngoingTickets',
                    'location', 'email')
    list_filter = ('department', 'name')
    readonly_fields = ['id', 'uuid', 'slug', 'numberOfOngoingTickets', ]
    actions = [make_qr_codes]
    #inlines = [TicketInLine, ]

    # Changing the add and change views so they display different fields

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            parent = obj.department
            parent.numberOfEntities -= 1
            parent.save()
            obj.delete()





    def add_view(self, request, extra_content=None):
        self.exclude = ('numberOfOngoingTickets',
                        'scanned', 'id', 'uuid', 'slug', 'qrCode',)
        return super(EntityAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        self.exclude = ('qrCode', 'quantity')
        return super(EntityAdmin, self).change_view(request, object_id)

# Methods for changing status of many tickets


def make_received(modeladmin, request, queryset):
    queryset.update(status='1')


def make_ongoing(modeladmin, request, queryset):
    queryset.update(status='2')


def make_dismissed(modeladmin, request, queryset):
    queryset.update(status='3')


def make_done(modeladmin, request, queryset):
    queryset.update(status='4')

def delete_selected_tickets(modeladmin, request, queryset):
        for obj in queryset:
            parent = obj.entity
            print('before' + str(parent.numberOfOngoingTickets))
            parent.numberOfOngoingTickets -= 1
            parent.save()
            obj.delete()
            print('after' + str(parent.numberOfOngoingTickets))




make_done.short_description = "Mark selected tickets as done"
make_dismissed.short_description = "Mark selected tickets as dismissed"
make_ongoing.short_description = "Mark selected tickets as ongoing"
make_received.short_description = "Mark selected tickets as received"


class TicketAdmin(admin.ModelAdmin):
    list_display = ['entity', 'room', 'department','type',
                    'message','location', 'created', 'status']
    list_filter = ('department', 'created', 'entity',)
    list_editable = ('status',)
    readonly_fields = ['location']
    actions = [make_done, make_received, make_dismissed, make_ongoing, delete_selected_tickets]

    

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(EntityType, EntityTypeAdmin)
admin.site.register(Room, RoomAdmin)


