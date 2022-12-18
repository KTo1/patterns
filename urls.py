from savraska.urls import Url
from views import IndexPage, Math, ContactPage, SchedulesPage

urlpatterns = [
    Url('^/$', IndexPage),
    Url('^/math.*$', Math),
    Url('^/contact/$', ContactPage),
    Url('^/schedules/$', SchedulesPage),
]