from waitress import serve
from savraska.main import Savraska
from urls import urlpatterns


app = Savraska(
    urls=urlpatterns
)
