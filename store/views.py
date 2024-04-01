from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .models import Product, Collection, OrderItem, CartItem, Cart
from .serializer import ProductSerializer, CollecctionSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItem

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'cannot delete this!'})
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        product_count=Count('product')).all()
    serializer_class = CollecctionSerializer

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(id=kwargs['pk']).count() > 0:
            return Response({'error': 'you cannot delete this'})
        return super().destroy(request, *args, **kwargs)


class CartViewSet(CreateModelMixin,
                RetrieveModelMixin,
                DestroyModelMixin,
                GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItem
        return CartItemSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart_id'] = self.kwargs['card_pk']
        return context
    
    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['card_pk']) \
            .select_related('product')