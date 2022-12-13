from savraska.urls import Url
from views import HomePage, Math


urlpatterns = [
    Url('^/$', HomePage),
    Url('^/math/$', Math),
]