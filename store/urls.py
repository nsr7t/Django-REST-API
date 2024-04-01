from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# URLConf
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('cards', views.CartViewSet)

card_router = routers.NestedDefaultRouter(router, 'cards', lookup='card')
card_router.register('items', views.CartItemViewSet, basename='card-item')

urlpatterns = router.urls + card_router.urls
