import django
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)

# URLConf
urlpatterns = router.urls

# urlpatterns = [
#    from django.urlls import include
#    path('', include(router.urls)),
#    other paths
# ]
