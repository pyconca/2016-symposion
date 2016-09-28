from django.core.management.base import BaseCommand, CommandError

from symposion.schedule.models import Presentation

class Command(BaseCommand):
    help = 'Copy Proposal content into scheduling Presentations'

    def handle(self, *args, **options):
        objs = Presentation.objects.\
                select_related('proposal_base').\
                order_by('proposal_base_id').\
                all()

        for pr in objs:
            pb = pr.proposal_base
            print('#{:03d} {}'.format(pr.proposal_base_id, pb.title))

            pr.title = pb.title
            pr.description = pb.description
            #pr.description_html = pb.description_html
            pr.abstract = pb.abstract
            #pr.abstract_html = pb.abstract_html

            pr.save()
