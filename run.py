from apps import create_app, celery

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        celery.start()
