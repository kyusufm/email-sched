from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_wtf.csrf import csrf_exempt


# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'  # Using SQLite for simplicity
db = SQLAlchemy(app)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Using Redis as the message broker
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Using Redis as the result backend
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define the database model
class Email(db.Model):
    __tablename__ = 'email'  # Explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email_subject = db.Column(db.String(255))
    email_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

# Celery task to send emails
@celery.task
def send_email(email_id):
    email = Email.query.get(email_id)
    # logic to send the email
    # print(f"Sending email to {email.email_subject} with content: {email.email_content}")
    print("Sending email to " + email.email_subject + " with content: " + email.email_content)

# Welcome endpoint
@app.route('/')
def index():
    return 'Welcome to the index page!'

# Endpoint to save emails
@app.route('/save_emails', methods=['POST'])
@csrf_exempt
def save_emails():
    data = request.json
    event_id = data.get('event_id')
    email_subject = data.get('email_subject')
    email_content = data.get('email_content')
    timestamp = datetime.strptime(data.get('timestamp'), '%d %b %Y %H:%M')

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
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
