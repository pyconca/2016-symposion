from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response

from symposion.conference.models import Conference, Section, current_conference
from symposion.schedule.models import Schedule, Session, Day, Room, Slot, SlotKind, SlotRoom, Presentation, SessionRole
from symposion2016.pycon_proposals.models import TalkProposal
from .serializers import TalkSerializer, ConferenceSerializer, SectionSerializer


# CONFERENCE

class ConferenceViewset(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    http_method_names = ('get', 'head', 'options',)


class CurrentConferenceView(views.APIView):
    http_method_names = ('get', 'head', 'options',)

    def get(self, request, format=None):
        conf = current_conference()
        conf_serializer = ConferenceSerializer(instance=conf)

        return Response(data=conf_serializer.data)


# SCHEDULE


class TalkProposalView(viewsets.ModelViewSet):
    queryset = TalkProposal.objects.all()
    serializer_class = TalkSerializer
    http_method_names = ('get', 'head', 'options',)
