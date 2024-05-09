from celery import Celery
from app import create_app, send_email

flask_app = create_app()
celery = Celery(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

if __name__ == '__main__':
    celery.start()