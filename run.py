from waitress import serve
from savraska.main import Savraska
from urls import urlpatterns

print('run at http://127.0.0.1:8000')

app = Savraska(
    urls=urlpatterns
)

serve(app, listen='127.0.0.1:8080')