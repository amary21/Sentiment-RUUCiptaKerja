from apps import create_app, celery

app = create_app(celery=celery)

if __name__ == "__main__":
    app.run(debug=True)
