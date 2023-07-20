import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Collection


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self, create_collection):
        response = create_collection({"title": "test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, create_collection):
        authenticate()

        response = create_collection({"title": "test"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=True)

        response = create_collection({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        authenticate(is_staff=True)

        response = create_collection({"title": "test"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count": 0,
        }

    def test_retrieve_collections_list(self, api_client):
        collections = baker.make(Collection, _quantity=10)

        response = api_client.get("/store/collections/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10

    def test_if_collection_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/store/collections/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_collection_has_products_returns_count(self, api_client):
        collection = baker.make(Collection)
        baker.make("Product", collection=collection, _quantity=5)

        response = api_client.get(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["products_count"] == 5


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_return_401(self, api_client):
        response = api_client.put("/store/collections/1/", {"title": "test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, api_client):
        authenticate()

        response = api_client.put("/store/collections/1/", {"title": "test"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.put(f"/store/collections/{collection.id}/", {"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_collection_does_not_exist_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.put("/store/collections/1/", {"title": "test"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_valid_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.put(f"/store/collections/{collection.id}/", {"title": "test"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == collection.id
        assert response.data["title"] == "test"


@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_user_is_anonymous_return_401(self, api_client):
        response = api_client.delete("/store/collections/1/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, api_client):
        authenticate()

        response = api_client.delete("/store/collections/1/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_does_not_exist_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.delete("/store/collections/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_collection_exists_returns_204(self, authenticate, api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.delete(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Collection.objects.filter(id=collection.id).exists() is False
