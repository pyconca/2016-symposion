import json
from datetime import time, datetime, timedelta

from symposion.schedule.models import *
from django.core.management.base import BaseCommand, CommandError

def add_time_delta(t, td):
    d1 = datetime.datetime(2000, 1, 1, t.hour, t.minute, t.second)
    d2 = d1 + td
    return d2.time()


def get_or_create_day_room_slots(rooms, data):
    grid = {}
    talk_kind = SlotKind.objects.get(label='talk')

    for date, start_times in data.items():
        day = Day.objects.get(date=date)

        room_slots = {}

        for room_name in rooms:
            room = Room.objects.get(name__endswith=room_name)
            slots = []

            for start_time, duration in start_times:
                start = time(*map(int, start_time.split(':')))
                end = add_time_delta(start, timedelta(minutes=duration))
                slot = None

                try:
                    sr = SlotRoom.objects.get(
                            room=room,
                            slot__day=day,
                            slot__kind=talk_kind,
                            slot__start=start,
                            slot__end=end)

                    slot = sr.slot
                except SlotRoom.DoesNotExist:
                    slot = Slot(
                            day=day,
                            kind=talk_kind,
                            start=start,
                            end=end)
                    slot.save()

                    sr = SlotRoom(
                            slot=slot,
                            room=room)
                    sr.save()

                slots.append((slot, duration))

            room_slots[room_name] = slots

        grid[date] = room_slots

    return grid


def assign_talk_to_presentations(slots, talks):
    for date, rooms in talks.items():
        for room_name, proposal_pks in rooms.items():
            room_slots = slots[date][room_name]

            for (slot, duration), pk in zip(room_slots, proposal_pks):
                print("%s %s %s #%03d (%d mins)" % (date, room_name, slot.start, pk or 0, duration))

                if pk is None:
                    print("\tSkipping")
                    continue

                pres = Presentation.objects.get(proposal_base__pk=pk)
                pres.slot = slot
                pres.save()


class Command(BaseCommand):
    help = 'Populate schedule slots from JSON source'

    def add_arguments(self, parser):
        parser.add_argument('infile', type=str)

    def handle(self, *args, **options):
        with open(options['infile'], 'r') as fobj:
            data = json.load(fobj)

        for block in data:
            slots = get_or_create_day_room_slots(block['rooms'], block['times'])
            assign_talk_to_presentations(slots, block['talks'])
