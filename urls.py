from savraska.urls import Url
from views import HomePage


urlpatterns = [
    Url('^$', HomePage),
]