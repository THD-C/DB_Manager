import pytest
from unittest.mock import MagicMock
from src.Service.User import User
from user.user_pb2 import RegResponse, AuthResponse

@pytest.fixture
def mock_session(mocker):
    return mocker.patch('src.DB.Session')

@pytest.fixture
def mock_user(mocker):
    return mocker.patch('src.DB.User')

@pytest.fixture
def mock_user_detail(mocker):
    return mocker.patch('src.DB.UserDetail')

def test_register_success(mock_user_detail, mock_user, mock_session):
    # Arrange
    mock_request = MagicMock()
    mock_context = MagicMock()
    mock_user_detail.create_model.return_value = MagicMock(ID=1)
    mock_user.create_model.return_value = MagicMock()
    mock_session.return_value.__enter__.return_value = MagicMock()

    user_service = User()

    # Act
    response = user_service.Register(mock_request, mock_context)

    # Assert
    assert isinstance(response, RegResponse)
    assert response.success
    mock_user_detail.create_model.assert_called_once_with(mock_user_detail, mock_request)
    mock_user.create_model.assert_called_once_with(mock_user, mock_request)

def test_register_failure(mock_user_detail, mock_user, mock_session):
    # Arrange
    mock_request = MagicMock()
    mock_context = MagicMock()
    mock_user_detail.create_model.return_value = MagicMock(ID=1)
    mock_user.create_model.return_value = MagicMock()
    mock_session.return_value.__enter__.side_effect = Exception("DB Error")

    user_service = User()

    # Act
    response = user_service.Register(mock_request, mock_context)

    # Assert
    assert isinstance(response, RegResponse)
    assert not response.success
    mock_user_detail.create_model.assert_called_once_with(mock_user_detail, mock_request)
    mock_user.create_model.assert_called_once_with(mock_user, mock_request)