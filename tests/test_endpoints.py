import json

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Welcome to the index page!'

def test_save_and_get_emails(client, clean_email_table):
    # Test saving an email
    data = {
        'event_id': 1,
        'email_subject': 'Test Email Subject',
        'email_content': 'This is a test email content',
        'timestamp': '15 Dec 2022 12:00'
    }
    response = client.post('/save_emails', json=data)
    assert response.status_code == 201

    # Test retrieving saved emails
    response = client.get('/emails')
    assert response.status_code == 200
    emails = json.loads(response.data.decode('utf-8'))
    assert len(emails) == 1
    assert emails[0]['event_id'] == 1
    assert emails[0]['email_subject'] == 'Test Email Subject'
    assert emails[0]['email_content'] == 'This is a test email content'
    assert emails[0]['timestamp'] == '15 Dec 2022 12:00'

