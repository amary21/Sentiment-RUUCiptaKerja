from apps import create_app, celery
from apps.extensions import ReverseProxied
from dotenv import dotenv_values

config = dotenv_values(".env")
app = create_app(celery=celery)

if __name__ == "__main__":
    fn = config.get("FLASK_ENV", "development")
    if fn == 'production':
        debug = False
        app.wsgi_app = ReverseProxied(app.wsgi_app)
    else:
        debug = True
    app.run(debug=debug)


