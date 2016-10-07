from rest_framework import serializers
from symposion.conference.models import Conference, Section
from symposion.speakers.models import Speaker
from symposion2016.pycon_proposals.models import TalkProposal


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section


class ConferenceSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField(read_only=True)
    sections = SectionSerializer(source='section_set', many=True, read_only=True)

    class Meta:
        model = Conference
        fields = ('id', 'title', 'start_date', 'end_date', 'timezone', 'sections')


class SpeakerSerialize(serializers.ModelSerializer):

    class Meta:
        model = Speaker


class TalkSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerialize()
    kind = serializers.SerializerMethodField()
    audience_level = serializers.SerializerMethodField()
    additional_speakers = SpeakerSerialize(many=True)

    class Meta:
        model = TalkProposal

    def get_kind(self, obj):
        return obj.kind.slug

    def get_audience_level(self, obj):
        return dict(TalkProposal.AUDIENCE_LEVELS).get(obj.audience_level, 'none')
