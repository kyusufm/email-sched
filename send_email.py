# send_emails.py

import time
from datetime import datetime
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_
from app import app, Email, Recipient, Event, event_recipients

# Initialize Flask app context
ctx = app.app_context()
ctx.push()

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Celery task to send emails
@celery.task
def send_email(email_id):
    email = Email.query.get(email_id)
    # Logic to send the email
    print("Sending email to " + email.email_subject + " with content: " + email.email_content)
    # Set email.sent = True after sending
    email.sent = True
    db.session.commit()

# Schedule Celery task to check for emails to send periodically
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every minute
    sender.add_periodic_task(
        60.0,
        check_and_send_emails.s(),
        name='check and send emails'
    )

@celery.task
def check_and_send_emails():
    current_time = datetime.now()
    emails_to_send = Email.query.filter(Email.timestamp <= current_time, Email.sent == False).all()
    for email in emails_to_send:
        event = email.event
        recipients = event.recipients
        for recipient in recipients:
            send_email.delay(email.id)

if __name__ == "__main__":
    celery.start()

