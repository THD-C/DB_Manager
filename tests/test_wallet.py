import pytest
from unittest.mock import MagicMock, patch
from src.Service.Wallet import Wallet
from wallet.wallet_pb2 import WalletID, Wallet as grpcWallet
from src import DB, Utils

@pytest.fixture
def mock_session(mocker):
    return mocker.patch('src.DB.Session')

@pytest.fixture
def mock_wallet(mocker):
    return mocker.patch('src.DB.Wallet')

@pytest.fixture
def mock_utils(mocker):
    return mocker.patch('src.Utils.create_grpc_model')

def test_delete_wallet_success(mock_session, mock_wallet, mock_utils):
    # Arrange
    mock_request = MagicMock(spec=WalletID)
    mock_request.id = 1
    mock_context = MagicMock()
    mock_wallet_instance = MagicMock()
    mock_session_instance = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_session_instance
    mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_wallet_instance

    wallet_service = Wallet()

    # Act
    response = wallet_service.deleteWallet(mock_request, mock_context)

    # Assert
    mock_session_instance.query.return_value.filter.assert_called_once_with(DB.Wallet.id == mock_request.id)
    mock_wallet_instance.delete.assert_called_once_with(mock_session_instance)
    mock_utils.assert_called_once_with(grpcWallet, mock_wallet_instance)
    assert response == mock_utils.return_value

def test_delete_wallet_not_found(mock_session, mock_wallet, mock_utils):
    # Arrange
    mock_request = MagicMock(spec=WalletID)
    mock_request.id = 1
    mock_context = MagicMock()
    mock_session_instance = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_session_instance
    mock_session_instance.query.return_value.filter.return_value.first.return_value = None

    wallet_service = Wallet()

    # Act
    response = wallet_service.deleteWallet(mock_request, mock_context)

    # Assert
    mock_session_instance.query.return_value.filter.assert_called_once_with(DB.Wallet.id == mock_request.id)
    mock_utils.assert_called_once_with(grpcWallet, None)
    assert response == mock_utils.return_value

def test_delete_wallet_exception(mock_session, mock_wallet, mock_utils):
    # Arrange
    mock_request = MagicMock(spec=WalletID)
    mock_request.id = 1
    mock_context = MagicMock()
    mock_wallet_instance = MagicMock()
    mock_session_instance = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_session_instance
    mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_wallet_instance
    mock_wallet_instance.delete.side_effect = Exception("DB Error")

    wallet_service = Wallet()

    # Act
    response = wallet_service.deleteWallet(mock_request, mock_context)

    # Assert
    mock_session_instance.query.return_value.filter.assert_called_once_with(DB.Wallet.id == mock_request.id)
    mock_wallet_instance.delete.assert_called_once_with(mock_session_instance)
    assert mock_wallet_instance.id is None
    mock_utils.assert_called_once_with(grpcWallet, mock_wallet_instance)
    assert response == mock_utils.return_value