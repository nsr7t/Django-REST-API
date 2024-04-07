from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from store.premission import IsAdminOrReadOnly
from .models import Customer, Product, Collection, OrderItem, CartItem, Cart
from .serializer import CustomerSerializer, ProductSerializer, CollecctionSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItem

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['title', 'unit_price'] 
    search_fields = ['title', 'unit_price']
    
    
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
    permission_classes = [IsAdminOrReadOnly]

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
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'],  permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    
# class CustomerViewSet(ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = [IsAdminUser]
#     @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         (customer, created) = Customer.objects.get_or_create(
#             user_id=request.user.id)
#         if request.method == 'GET':
#             serializer = CustomerSerializer(customer)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = CustomerSerializer(customer, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)