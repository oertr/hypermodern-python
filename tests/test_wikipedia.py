from typing import Mock

import click
import pytest

from hypermodern_python import wikipedia


def test_random_page_returns_page(mock_requests_get: Mock) -> None:
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()