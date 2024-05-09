from datetime import datetime

class Email:
    def __init__(self, event_id, email_subject, email_content, timestamp):
        self.event_id = event_id
        self.email_subject = email_subject
        self.email_content = email_content
        self.timestamp = timestamp