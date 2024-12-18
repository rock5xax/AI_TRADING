import pytest
from services.session_service import SessionService
from breeze_connect import BreezeConnect


@pytest.fixture
def session_service():
    return SessionService(api_key="dummy_api_key")


def test_generate_session_token_success(mocker, session_service):
    mock_client = mocker.Mock(spec=BreezeConnect)
    mocker.patch("services.session_service.BreezeConnect", return_value=mock_client)
    mock_client.generate_session.return_value = None

    client = session_service.generate_session_token("dummy_api_secret", "dummy_token")
    assert client == mock_client
    mock_client.generate_session.assert_called_once_with(api_secret="dummy_api_secret", session_token="dummy_token")


def test_generate_session_token_failure(mocker, session_service):
    mock_client = mocker.Mock(spec=BreezeConnect)
    mocker.patch("services.session_service.BreezeConnect", return_value=mock_client)
    mock_client.generate_session.side_effect = Exception("Invalid token")

    with pytest.raises(ValueError, match="Failed to generate session token: Invalid token"):
        session_service.generate_session_token("dummy_api_secret", "invalid_token")


def test_validate_session(session_service):
    assert session_service.validate_session("valid_token") is True
    assert session_service.validate_session("") is False
