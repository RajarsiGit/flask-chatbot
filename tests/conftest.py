import pytest

from app import create_app


class FakeBot:
    def get_response(self, text):
        return "echo: {}".format(text)


@pytest.fixture
def app():
    flask_app = create_app(bot=FakeBot())
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
