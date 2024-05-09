import pytest
from app import app, db, Email

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def clean_email_table():
    """Fixture to empty the email table before running tests."""
    # Delete all rows from the email table
    db.session.query(Email).delete()
    db.session.commit()