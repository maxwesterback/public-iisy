from django.forms import modelformset_factory
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Department
from .models import Entity
from .models import Ticket
from .models import Room

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
# to get customer
from django.db import connection
# Rest API stuff
from .serializers import DepartmentSerializer
from .serializers import EntityListSerializer
from .serializers import EntityCreateSerializer
from .serializers import EntityRetrieveUpdateSerializer
from .serializers import TicketListSerializer
from .serializers import TicketCreateSerializer
from .serializers import TicketStatusUpdateSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# external libraries
import numpy as np
from datetime import datetime, timezone
from dateutil import tz
import plotly.offline as opy
import plotly.graph_objs as go
from Customer.models import Client
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail


def company_page(request):
    return render(request, 'company_page/index.html')


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def landing(request, object_uuid):
    context = {'object': object_uuid}
    customer = connection.get_tenant()
    # Must do this before we change context to contain name, otherwise ticket can't be created
    request.session['context'] = context
    try:
        entity = Entity.objects.get(uuid=object_uuid)       
        context = {'customer': customer, 'object': entity}
        return render(request, 'home_app/index.html', context)
    except Entity.DoesNotExist:
        print(str(object_uuid))

        room = Room.objects.get(uuid=object_uuid)
        context = {'customer': customer, 'object': room}
        return render(request, 'home_app/indexRoom.html', context)



def register_ticket(request):
    context = request.session.get('context', None)
    object_uuid = context['object']
    print(str(request.POST))

    try:
        canSend = False
        entity = Entity.objects.filter(uuid=object_uuid).first()
        if entity is None:
            room = Room.objects.filter(uuid=object_uuid).first()
            tickets = Ticket.objects.filter(room=room)
            if(tickets.count() != 0):
                lastTicket = tickets.reverse()[0]
                now = datetime.now(timezone.utc)
                deltaTime = now - lastTicket.created
                days, seconds = deltaTime.days, deltaTime.seconds
                hours = days * 24 + seconds // 3600
                print("hours between last ticket " + str(hours))
            else:
                canSend = True
            if room.location == "1":
                return redirect('http://' + str(connection.get_tenant().prefix) + '.newdomain.live/admin/iisy_landing/room/' + str(room.id) + '/change/')

            if(canSend or hours >= room.hoursBetweenTickets):
                for types in room.types.all():
                    print("TYPES IN THIS ROOM ARE " + types.name)
                    if types.name in request.POST:
                        print('found type!')
                        message = 'Issue received for an object of type: ' + types.name + ' in the: ' + room.name + ' in ' + room.location

                        ticket = Ticket.objects.create(
                                room=room, isRoom=True, message=message, type=types.name
                            )                    
                        room.lastTicket = datetime.now()
                        print("sent to " + types.email)
                        send_mail('Issue reported from IISY',
                                message,
                                'IISYapplication@gmail.com',
                                [types.email],
                                fail_silently=False)

            else:
                print("Ticket too recent")
        else:

            message = 'Issue received for ' + entity.name + ' in location ' + entity.location

            tickets = Ticket.objects.filter(entity=entity)
            if(tickets.count() != 0):
                lastTicket = tickets.reverse()[0]
                now = datetime.now(timezone.utc)
                deltaTime = now - lastTicket.created
                days, seconds = deltaTime.days, deltaTime.seconds
                hours = days * 24 + seconds // 3600
                print("hours between last ticket " + str(hours))
            else:
                canSend = True
            if entity.location == "1":
                return redirect('http://' + str(connection.get_tenant().prefix) + '.newdomain.live/admin/iisy_landing/entity/' + str(entity.id) + '/change/')

            if(canSend or hours >= entity.hoursBetweenTickets):
                if entity.shouldHaveTextBox:
                    message = request.POST.get('description')

                    ticket = Ticket.objects.create(
                        entity=entity,
                        message=message,
                        type=entity.entityType
                    )
                else:
                    ticket = Ticket.objects.create(
                        entity=entity,
                        type=entity.entityType

                    )
                entity.lastTicket = datetime.now()
                print("sent to " + entity.email)

                send_mail('Issue reported from IISY',
                        message,
                        'IISYapplication@gmail.com',
                        [entity.email],
                        fail_silently=False)

            else:
                print("Ticket too recent")

    except Exception as e:
        print(str(e))
    return render(request, 'home_app/new_ticket.html')


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# For creating/getting departments, entities, etc
# The serializer converts the JSON received to a model
class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)


class SingleDepartmentView(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EntityList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)

    queryset = Entity.objects.all()
    serializer_class = EntityListSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)


class EntityListCreate(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    queryset = Entity.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = EntityCreateSerializer
        elif self.request.method == 'GET':
            serializer_class = EntityListSerializer

        return serializer_class

# get single entity by id


class SingleEntityView(generics.RetrieveUpdateAPIView):
    #permission_classes = (IsAuthenticated,)

    queryset = Entity.objects.all()
    serializer_class = EntityRetrieveUpdateSerializer

# get all or POST one ticket


class TicketListCreate(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = TicketCreateSerializer
        elif self.request.method == 'GET':
            serializer_class = TicketListSerializer

        return serializer_class

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)


# get/update single ticket by id
class SingleTicketView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusUpdateSerializer


class Graph(LoginRequiredMixin, TemplateView):
    template_name = 'home_app/chart.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        def utc_to_local(utc_dt):
            return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=tz.gettz('Europe/Helsinki'))

        context = super(Graph, self).get_context_data(**kwargs)

        MY_CHOICES = {
            '1': 'Received',
            '2': 'Ongoing',
            '3': 'Dismissed',
            '4': 'Done'
        }
        TICKET_CHOICES = {
            '1': 'Fix',
            '2': 'Replace',
            '3': 'Empty',
            '4': '----'
        }

        created = Ticket.objects.values_list(
            'created', flat=True).order_by('created')
        status = Ticket.objects.values_list(
            'status', flat=True).order_by('created')
        message = Ticket.objects.values_list(
            'message', flat=True).order_by('created')
        location = Ticket.objects.values_list(
            'location', flat=True).order_by('created')
        entity = Ticket.objects.first().entity
        tickets = Ticket.objects.order_by('created')
        x = [utc_to_local(d) for d in created]
        #y = np.ones((len(x),), dtype=int)
        y = [l for l in location]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'size': 10},
                            mode="markers",  name='1st Trace')

        layout = go.Layout(title="Latest issues for " + entity.department, xaxis={
                           'title': 'Date'}, yaxis={'title': 'Issues', })
        figure = go.Figure(data=trace1, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        table_data = go.Table(header=dict(
            values=['Created', 'Status', 'Message', 'Location']),
            cells=dict(values=[
                [d.strftime("%a,%d %B, %Y") for d in created],
                [MY_CHOICES[s] for s in status],
                [TICKET_CHOICES[m] for m in message],
                [l for l in location],
                [n.entity.name for n in tickets]
            ])
        )
        table_figure = go.Figure(data=table_data)
        table_figure.update_layout(title_text='Status')

        table_div = opy.plot(table_figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['table'] = table_div

        return context
