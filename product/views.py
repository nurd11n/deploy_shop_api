from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from review.models import Like
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# class CategoryView(APIView):
#
#     def get(self, request):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(instance=queryset, many=True)
#         return Response(serializer.data, status=200)
#
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)
#
#
# class CategoryDetailView(APIView):
#
#     def get_object(self, pk):
#         try:
#             category = Category.objects.get(slug=pk)
#             return category
#         except Category.DoesNotExist:
#             raise Http404
#
#     def put(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(instance=category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=200)
#
#     def get(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(instance=category)
#         return Response(serializer.data, status=200)
#
#     def delete(self, request, pk):
#         category = self.get_object(pk)
#         category.delete()
#         return Response('Successfully deleted', status=204)
#
#
# class ProductView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CategoryView(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(PermissionMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'price', 'category']
    search_fields = ['title', 'created_at', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductDetailSerializer
        return self.serializer_class

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(product=product, author=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(product=product, author=user)
            like.save()
            message = 'liked'
        return Response(message)

