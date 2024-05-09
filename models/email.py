from extensions import db

class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email_subject = db.Column(db.String(255))
    email_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)