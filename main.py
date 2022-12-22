import os

from savraska.main import Savraska
# from urls import urlpatterns
from views import urlpatterns
from savraska.middleware import middlewares


settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR_NAME': 'templates',
    'STATIC_DIR_NAME': 'static',
}


app = Savraska(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares,
)
