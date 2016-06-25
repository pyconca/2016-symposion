from rest_framework import serializers
from symposion.conference.models import Conference, Section
from symposion.schedule.models import Schedule, Session, Day, Room, Slot, SlotKind, SlotRoom, Presentation, SessionRole


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section


class ConferenceSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField(read_only=True)
    sections = SectionSerializer(source='section_set', many=True, read_only=True)

    class Meta:
        model = Conference
        fields = ('id', 'title', 'start_date', 'end_date', 'timezone', 'sections')


class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Day


class ScheduleSerializer(serializers.ModelSerializer):
    section = SectionSerializer(read_only=True)
    dates = DaySerializer(source='day_set', read_only=True, many=True)
    slot_kinds = serializers.SerializerMethodField()
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = Schedule

    def get_slot_kinds(self, obj):
        return obj.slotkind_set.all().values_list('label', flat=True)

    def get_rooms(self, obj):
        return obj.room_set.all().values_list('name', flat=True)


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room


class SlotSerializer(serializers.ModelSerializer):
    day = DaySerializer(read_only=True)
    kind = serializers.CharField(source='kind__label', read_only=True)

    class Meta:
        model = Slot


class PresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
