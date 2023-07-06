from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    @pytest.mark.skip
    def test_if_user_is_anonymous_return_401(self):
        # Arrange
        """Noting to arrange here"""

        # Act
        client = APIClient()
        response = client.post("/collections/", {"title": "test"})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
