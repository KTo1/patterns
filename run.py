from main import app

# waitress-serve --listen=127.0.0.1:8000 main:app

print('run at http://127.0.0.1:8000')

serve(app, listen='127.0.0.1:8080')