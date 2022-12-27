from waitress import serve

from main import app_debug

# waitress-serve --listen=127.0.0.1:8000 main:app

print('run at http://127.0.0.1:8000')

serve(app_debug, listen='127.0.0.1:8000')