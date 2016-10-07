from django.conf.urls import patterns, include, url

from rest_framework import routers

from .views import ConferenceViewset, CurrentConferenceView, TalkProposalView

router = routers.DefaultRouter()
router.register(r'conferences', ConferenceViewset)
router.register(r'proposals', TalkProposalView)


urlpatterns = patterns(
    "",
    url(r'^', include(router.urls)),
    url(r'^conference$', CurrentConferenceView.as_view(), name='current_conference'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
)