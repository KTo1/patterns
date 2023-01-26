import os

from savraska.main import Savraska, SavraskaFake, SavraskaDebug
# from urls import urlpatterns
from views import urlpatterns
from savraska.middleware import middlewares


settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR_NAME': 'templates',
    'STATIC_DIR_NAME': 'staticfiles',
    'STATIC_URL': 'static'
}


app = Savraska(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares,
)

app_fake = SavraskaFake(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares,
)

app_debug = SavraskaDebug(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares,
)