"""
Copyright (c) 2010-2014, Eldarion, Inc. and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    * Neither the name of Eldarion, Inc. nor the names of its contributors may
      be used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import unicode_literals
import itertools

from django.db.models import Count, Min

from symposion.schedule.models import Room, Slot, SlotRoom


class TimeTable(object):

    def __init__(self, day):
        self.day = day

    def slots_qs(self):
        qs = Slot.objects.all()
        qs = qs.filter(day=self.day)
        return qs

    def rooms(self):
        qs = Room.objects.all()
        #qs = qs.filter(schedule=self.day.schedule)
        qs = qs.filter(
            pk__in=SlotRoom.objects.filter(slot__in=self.slots_qs().values("pk")).values("room"))
        qs = qs.order_by("order")
        return qs

    def __iter__(self):
        times = sorted(set(itertools.chain(*self.slots_qs().values_list("start", "end"))))
        slots = Slot.objects.filter(pk__in=self.slots_qs().values("pk"))
        slots = slots.annotate(room_count=Count("slotroom"), order=Min("slotroom__room__order"))
        slots = slots.order_by("start", "order")
        row = []
        for time, next_time in pairwise(times):
            row = {"time": time, "slots": []}
            for slot in slots:
                if slot.start == time:
                    slot.rowspan = TimeTable.rowspan(times, slot.start, slot.end)
                    slot.colspan = slot.room_count
                    row["slots"].append(slot)
            if row["slots"] or next_time is None:
                yield row

    @staticmethod
    def rowspan(times, start, end):
        return times.index(end) - times.index(start)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b)
    return zip(a, b)
