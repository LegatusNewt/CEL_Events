import pytest
from communityenergylabsserver.flaskr import create_app
from communityenergylabsserver.seed import seed_test_events

@pytest.fixture
def client():
    app = create_app()
    seed_test_events()
    yield app.test_client()