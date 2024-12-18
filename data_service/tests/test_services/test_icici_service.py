import pytest
from services.icici_service import ICICIService


@pytest.fixture
def icici_service():
    return ICICIService()


def test_get_order_book_success(mocker, icici_service):
    mock_client = mocker.Mock()
    mock_client.get_order_book.return_value = {"orders": [{"id": 1, "status": "completed"}]}
    mocker.patch.object(icici_service, "client", mock_client)

    orders = icici_service.get_order_book()
    assert len(orders["orders"]) == 1
    assert orders["orders"][0]["status"] == "completed"


def test_get_order_book_failure(mocker, icici_service):
    mock_client = mocker.Mock()
    mock_client.get_order_book.side_effect = Exception("API Error")
    mocker.patch.object(icici_service, "client", mock_client)

    with pytest.raises(Exception, match="API Error"):
        icici_service.get_order_book()
