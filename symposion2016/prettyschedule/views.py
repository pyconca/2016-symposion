from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from symposion.schedule.models import Day, Presentation

from timetable import TimeTable

class ScheduleView(TemplateView):
    template_name = 'prettyschedule/schedule.html'

    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise Http404()

        days_qs = Day.objects.all()
        days = [ TimeTable(day) for day in days_qs ]

        return self.render_to_response({
            'days': days
        })


class PresentationView(TemplateView):
    template_name = 'prettyschedule/presentation.html'

    def get(self, request, pk, *args, **kwargs):
        presentation = get_object_or_404(Presentation, pk=pk)

        return self.render_to_response({
            'p': presentation
        })
