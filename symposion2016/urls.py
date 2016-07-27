from collections import OrderedDict

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
from account.views import LoginView, SignupView
from account.forms import SignupForm
from account.forms import LoginEmailForm
from django.contrib.auth import get_user_model

import symposion.views


WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"


class LoginEmailView(LoginView):
    form_class = LoginEmailForm


class NoUsernameSignUpForm(SignupForm):
    username = None

    def __init__(self, *args, **kwargs):
        super(NoUsernameSignUpForm, self).__init__(*args, **kwargs)

        order = ['email', 'password', 'password_confirm', 'code']
        self.fields = OrderedDict(sorted(self.fields.items(),
                                         key=lambda t: order.index(t[0]) if t[0] in order else len(order)))


class NoUsernameSignUpView(SignupView):
    form_class = NoUsernameSignUpForm

    def generate_username(self, form):
        email = form.cleaned_data['email']
        new_username = email.split('@')[0]
        User = get_user_model()
        c = 1
        while User.objects.filter(username=new_username+str(c)).exists():
            c += 1

        return new_username + str(c)

urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),

    # url(r"^account/signup/$", symposion.views.SignupView.as_view(), name="account_signup"),
    # url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
    url(r"^account/login/$", LoginEmailView.as_view(), name="account_login"),
    url(r"^account/signup/$", NoUsernameSignUpView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),

    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^teams/", include("symposion.teams.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),
    url(r"^markitup/", include("markitup.urls")),
    url(r"^boxes/", include("pinax.boxes.urls")),

    # url(r"^", include("symposion.cms.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
