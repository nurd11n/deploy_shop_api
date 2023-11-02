from django.urls import path
from .views import CategoryView, ProductView
from rest_framework.routers import DefaultRouter
from django.urls import include


router = DefaultRouter()
router.register('categories', CategoryView)
router.register('products', ProductView)

urlpatterns = [
    path('', include(router.urls))

    # path('categories/', CategoryView.as_view({'get': 'list', 'post': 'create'})),
    # path('categories/<slug:pk>/', CategoryView.as_view({'get': 'retrieve',
    #                                                     'put': 'update',
    #                                                     'patch': 'partial_update',
    #                                                     'delete': 'destroy'})),
    # path('products/', ProductView.as_view({'get': 'list', 'post': 'create'})),
    # path('products/<slug:pk>/', ProductView.as_view({'get': 'retrieve',
    #                                                  'put': 'update',
    #                                                  'patch': 'partial_update',
    #                                                  'delete': 'destroy'}))

]