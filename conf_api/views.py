from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response

from symposion.conference.models import Conference, Section, current_conference
from symposion.schedule.models import Schedule, Session, Day, Room, Slot, SlotKind, SlotRoom, Presentation, SessionRole
from .serializers import ConferenceSerializer, ScheduleSerializer, SlotSerializer


# CONFERENCE

class ConferenceViewset(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class CurrentConferenceView(views.APIView):

    def get(self, request, format=None):
        conf = current_conference()
        conf_serializer = ConferenceSerializer(instance=conf)

        return Response(data=conf_serializer.data)


# SCHEDULE


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        qs = super(ScheduleViewSet, self).get_queryset()
        return qs.filter(section__conference=current_conference())


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
