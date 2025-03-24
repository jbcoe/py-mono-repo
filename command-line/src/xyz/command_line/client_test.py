"""Tests for the command-line client."""

import json
from unittest.mock import MagicMock, patch

from xyz.command_line.client import get_greeting


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_success(mock_get: MagicMock) -> None:
    """Test getting a greeting with a successful API response."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"greeting": "Hello, Test User!"}
    mock_get.return_value = mock_response

    result: str = get_greeting("Test User", host="localhost", port=8000)

    assert result == "Hello, Test User!"
    mock_get.assert_called_once_with("http://localhost:8000/greet/Test User", timeout=5)
    mock_response.raise_for_status.assert_called_once()
    mock_response.json.assert_called_once()


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_connection_error(mock_get: MagicMock) -> None:
    """Test handling of connection errors."""
    mock_get.side_effect = Exception("Connection refused")

    result: str = get_greeting("Test User", host="localhost", port=8000)

    assert "Error:" in result
    assert "Connection refused" in result


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_http_error(mock_get: MagicMock) -> None:
    """Test handling of HTTP errors."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("404 Not Found")
    mock_get.return_value = mock_response

    result: str = get_greeting("Test User", host="localhost", port=8000)

    assert "Error:" in result
    assert "404 Not Found" in result


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_with_server_url(mock_get: MagicMock) -> None:
    """Test getting a greeting with a custom server URL."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "greeting": "Hello from custom server, Test User!"
    }
    mock_get.return_value = mock_response

    result: str = get_greeting("Test User", server_url="https://example.com/api")

    assert result == "Hello from custom server, Test User!"
    mock_get.assert_called_once_with(
        "https://example.com/api/greet/Test User", timeout=5
    )


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_timeout(mock_get: MagicMock) -> None:
    """Test handling of request timeouts."""
    mock_get.side_effect = Exception("Connection timed out")

    result: str = get_greeting("Test User", host="localhost", port=8000)

    assert "Error:" in result
    assert "Connection timed out" in result


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_invalid_json(mock_get: MagicMock) -> None:
    """Test handling of invalid JSON responses."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    mock_get.return_value = mock_response

    result: str = get_greeting("Test User", host="localhost", port=8000)

    assert "Error:" in result
    assert "Invalid JSON" in result


@patch("xyz.command_line.client.requests.get")
def test_get_greeting_missing_field(mock_get: MagicMock) -> None:
    """Test fallback to default greeting when the API response is missing the greeting field."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Some other message"}
    mock_get.return_value = mock_response

    result: str = get_greeting("Test User", host="localhost", port=8000)

    assert result == "Hello, Test User!"  # Should fall back to default greeting
    mock_get.assert_called_once()
