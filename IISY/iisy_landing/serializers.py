# For converting JSON to model and vice versa
from rest_framework import serializers
from .models import Department
from .models import Entity
from .models import Ticket


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EntityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class EntityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['name', 'department']


class EntityRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['entity']


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status']
