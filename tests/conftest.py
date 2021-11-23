"""Package-wide test fixture."""
from unittest.mock import Mock

from _pytest.config import Config
import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_requests_get(mocker: MockerFixture) -> Mock:
    """Fixture for mocking requests.get."""
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


def pytest_configure(config: Config) -> None:
    """Configuration for e2e test."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
