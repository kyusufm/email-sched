from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_wtf.csrf import CSRFProtect
from utils.helpers import reformat_datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import and_


# Initialize Flask app
app = Flask(__name__)

# Configure CSRF protection
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection globally

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'  # Using SQLite for simplicity
db = SQLAlchemy(app)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Using Redis as the message broker
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Using Redis as the result backend
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define the database model
# Define the association table
event_recipients = db.Table('event_recipients',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('recipient_id', db.Integer, db.ForeignKey('recipients.id')),
    db.Column('sent', db.Boolean, default=False)
)
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    recipients = db.relationship('Recipient', secondary=event_recipients, backref='events')
class Recipient(db.Model):
    __tablename__ = 'recipients'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
class Email(db.Model):
    __tablename__ = 'email'  # Explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = relationship("Event", foreign_keys=[event_id], backref="emails")
    email_subject = db.Column(db.String(255))
    email_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

db.create_all()

# Celery task to send emails
@celery.task
def send_email(email_id):
    email = Email.query.get(email_id)
    event = email.event
    
    # Get recipients for the event from event_recipients table
    recipients = Recipient.query.join(event_recipients).filter(event_recipients.c.event_id == event.id).all()

    for recipient in recipients:
        # Logic to send email to each recipient
        print("Sending email to {} with subject: {} and content: {}".format(recipient.email, email.email_subject, email.email_content))
    
        # Update sent status for the recipient
        event_recipients.update().where(
            and_(
                event_recipients.c.event_id == event.id,
                event_recipients.c.recipient_id == recipient.id
            )
        ).values(sent=True)
        db.session.commit()

# Welcome endpoint
@app.route('/')
def index():
    return 'Welcome to the index page!'

# Endpoint to save emails
@app.route('/save_emails', methods=['POST'])
def save_emails():
    data = request.json
    event_id = data.get('event_id')
    email_subject = data.get('email_subject')
    email_content = data.get('email_content')

    # Reformat the datetime string using the reformat_datetime helper function
    timestamp = reformat_datetime(data.get('timestamp'))

    if not all([event_id, email_subject, email_content, timestamp]):
        return jsonify({'error': 'Missing required parameters'}), 400

    new_email = Email(event_id=event_id, email_subject=email_subject, email_content=email_content, timestamp=timestamp)
    db.session.add(new_email)
    db.session.commit()

    # Schedule the email to be sent at the specified timestamp
    send_email.apply_async((new_email.id,), eta=timestamp)

    return jsonify({'message': 'Email saved successfully'}), 201

# Endpoint to display all emails
@app.route('/emails', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    email_list = []
    for email in emails:
        email_list.append({
            'id': email.id,
            'event_id': email.event_id,
            'email_subject': email.email_subject,
            'email_content': email.email_content,
            'timestamp': email.timestamp.strftime('%d %b %Y %H:%M')
        })
    return jsonify(email_list)

# Create database tables if not exists and run the app
if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
