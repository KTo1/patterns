from savraska.urls import Url
from views import IndexPage, Math, ContactPage, SchedulesPage, CoursePage

urlpatterns = [
    Url('^/$', IndexPage),
    Url('^/math.*$', Math),
    Url('^/contact/$', ContactPage),
    Url('^/schedules/$', SchedulesPage),
    Url('^/courses/$', CoursePage),
]