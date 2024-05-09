from datetime import datetime
from app import Recipient, db, Event

def add_dummy_data():
    db.session.add(Recipient(email="jeff@gmail.com"))
    db.session.add(Recipient(email="mark@gmail.com"))
    db.session.add(Recipient(email="sergey@gmail.com"))

    # Commit the changes to the database
    db.session.commit()

    # Retrieve the IDs of the recipients
    recipient1_id = Recipient.query.filter_by(email="jeff@gmail.com").first().id
    recipient2_id = Recipient.query.filter_by(email="mark@gmail.com").first().id
    recipient3_id = Recipient.query.filter_by(email="sergey@gmail.com").first().id

    # Add dummy data to events table
    event = Event(event_name="Dummy Event", event_date=datetime.now())

    # Create relations between event and recipients
    event.recipients.append(Recipient.query.get(recipient1_id))
    event.recipients.append(Recipient.query.get(recipient2_id))
    event.recipients.append(Recipient.query.get(recipient3_id))

    # Commit the changes to the database
    db.session.add(event)
    db.session.commit()

if __name__ == "__main__":
    add_dummy_data()