from savraska.urls import Url
from views import IndexPage, Math, AboutPage, MailPage, StaticPages

urlpatterns = [
    Url('^/$', IndexPage),
    Url('^/math.*$', Math),
    Url('^/about/$', AboutPage),
    Url('^/mail/$', MailPage),
]