import pytest

from stock_correlations import create_app


class MockConfig:
    WTF_CSRF_ENABLED = False


@pytest.fixture
def mock_client():
    app = create_app(MockConfig)
    app.config.update(TESTING=True)

    with app.test_client() as client:
        yield client


def test_home(mock_client):
    """Test the home route."""
    response = mock_client.get('/')
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_about(mock_client):
    """Test the home route."""
    response = mock_client.get('/about')
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


# @pytest.fixture
# def mock_render_template(mocker):
#     """Mock render_template to return plain error messages instead of rendering HTML."""
#     mocker.patch("stock_correlations.routes.render_template", side_effect=lambda template, error_message: error_message)
#
#
# def test_verify_ticker_with_numbers(client):
#     """Test that a ticker containing non-alphabetic characters returns a 400 error."""
#     response = client.post("/verify", json={"ticker": "AAPL123"})
#
#     assert response.status_code == 400
#     assert b"Invalid ticker: Make sure the ticker contains only alpha characters and no spaces." in response.data
