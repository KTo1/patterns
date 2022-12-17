from savraska.urls import Url
from views import HomePage, Math, AboutPage, MailPage

urlpatterns = [
    Url('^/$', HomePage),
    Url('^/math.*$', Math),
    Url('^/about/$', AboutPage),
    Url('^/mail/$', MailPage),
]