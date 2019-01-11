"""
Definition of urls for Portal.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin

# 2018-10-26 no longer necessary as autodiscover automatically finds everything. Might not even be necessary to call autodiscover any more as it supposedly runs automatically.

# from Portal.app.models import User, Group, MemberOf, Files, FilesSent, Term, FundingStream, FeeScale, Setting, SettingDay, SettingFees, Pupil, PupilSessions
# admin.site.register(User)
# admin.site.register(Group)
# admin.site.register(MemberOf)
# admin.site.register(Files)
# admin.site.register(FilesSent)
# admin.site.register(Term)
# admin.site.register(FundingStream)
# admin.site.register(FeeScale)
# admin.site.register(Setting)
# admin.site.register(SettingDay)
# admin.site.register(SettingFees)
# admin.site.register(Pupil)
# admin.site.register(PupilSessions)

from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    # url( r'^login/$',auth_views.LoginView.as_view(template_name="useraccounts/login.html"), name="login"),
    url(r'^login/$',
        django.contrib.auth.views.LoginView,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.LogoutView,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
