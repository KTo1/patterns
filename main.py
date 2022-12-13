import os

from savraska.main import Savraska
from urls import urlpatterns


settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR_NAME': 'templates'
}


app = Savraska(
    urls=urlpatterns,
    settings=settings
)
