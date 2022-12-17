from savraska.urls import Url
from views import IndexPage, Math, AboutPage, ContactPage

urlpatterns = [
    Url('^/$', IndexPage),
    Url('^/math.*$', Math),
    Url('^/about/$', AboutPage),
    Url('^/contact/$', ContactPage),
]