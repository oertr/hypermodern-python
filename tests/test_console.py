"""Test cases for the console module."""
from unittest.mock import Mock

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from hypermodern_python import console, wikipedia


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for click.testing.CliRunner."""
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    """Fixture for request."""
    return mocker.patch("hypermodern_python.wikipedia.random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It prints the title of the Wikipedia page."""
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It invokes reuests.get."""
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It uses the English Wikipedia by default."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It exits with a non-zero status code if the requests fails."""
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It prints an error message if the request fails."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_random_page_uses_given_language(mock_requests_get: Mock) -> None:
    """It uses 'de.wikipedia.org' if pass a language='de'."""
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]


def test_main_uses_specified_language(runner: CliRunner, mock_wikipedia_random_page):
    """It invokes random_page with 'pl' language arg if pass cli a --language=pl."""
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner):
    """It exits a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
