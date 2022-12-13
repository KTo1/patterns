from savraska.urls import Url
from views import HomePage, Math, AboutPage

urlpatterns = [
    Url('^/$', HomePage),
    Url('^/math.*$', Math),
    Url('^/about/$', AboutPage),
]