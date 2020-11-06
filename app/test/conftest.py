import os

import pytest

from app.main import create_app


@pytest.fixture
def app():
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    return app
