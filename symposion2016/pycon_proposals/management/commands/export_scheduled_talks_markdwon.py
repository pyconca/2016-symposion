import os

from django.core.management.base import BaseCommand, CommandError

from symposion.schedule.models import Slot, SlotKind
from symposion.reviews.models import ProposalResult
from symposion2016.pycon_proposals.models import TalkProposal

class Command(BaseCommand):
    help = 'Export scheduled talks in Markdown format'

    CLEANUP_REPLACEMENTS = [
            ( u'\u2019', u"'" ),
            ]

    TALK_OUTPUT_FMT = ur'''
---
pk: {pk}
title: {title}
kind: {kind}
speakers: {speakers}
date: {date}
start_time: {start_time}
end_time: {end_time}
rooms: {rooms}
---

{body}

'''

    FILENAME_FMT = ur'''{pk:03d}-{speakers}-en.md'''

    @classmethod
    def cleanup(cls, s):
        s = s.strip()

        for old, new in cls.CLEANUP_REPLACEMENTS:
            s = s.replace(old, new)

        return s

    @staticmethod
    def to_filename(name):
        return name.lower().replace(' ', '_').replace("'", '').replace('.', '')

    def add_arguments(self, parser):
        parser.add_argument('outdir', type=str, default='.')

    def handle(self, *args, **options):
        outdir = options['outdir']

        slots = Slot.objects.all().select_related('day', 'kind', 'content_ptr')

        dividers = []

        for slot in slots:
            pres = slot.content
            if pres is not None:
                self.export_talk(outdir, slot, pres)

    def export_talk(self, outdir, slot, pres):
        pk = pres.proposal_base_id
        title = pres.title
        kind = slot.kind.label
        speakers = u'[' + u', '.join(s.name for s in pres.speakers()) + u']'
        date = slot.day.date
        start_time = slot.start
        end_time = slot.end
        rooms = u'[' + u', '.join(r.name for r in slot.rooms) + u']'
        body = pres.description

        output = self.TALK_OUTPUT_FMT.lstrip().format(**locals())

        for s in pres.speakers():
            output += u"## {} Bio\n\n".format(s.name)
            output += s.biography + u"\n\n"

        output = output.rstrip()

        filename_speakers = '-'.join([ self.to_filename(s.name) for s in pres.speakers() ])

        filename = self.FILENAME_FMT.format(pk=pk, speakers=filename_speakers)

        filepath = os.path.join(outdir, filename)
        with open(filepath, 'wb') as fobj:
            fobj.write(output.encode('utf-8'))
