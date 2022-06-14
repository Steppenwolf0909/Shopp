from django.urls import include, re_path, path
from . import views

urlpatterns = [
    path('all/', views.ListProductsAPIView.as_view(), name='get_products'),
    path('detail/<str:pk>/', views.DetailProductAPIView.as_view(), name='detail_products'),
    re_path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('get_favorite/', views.ListFavoriteAPIView.as_view(), name='get_favorite'),
    path('create_favorite/', views.CreateFavoriteAPIView.as_view(), name='create_favorite'),
    path('delete_favorite/', views.DeleteFavoriteAPIView.as_view(), name='delete_favorite'),
    path('create_product/', views.CreateProductAPIView.as_view(), name='create_product'),
    path('delete_product/<str:pk>/', views.DeleteProductAPIView.as_view(), name='delete_product'),
    path('update_product/', views.UpdateProductAPIView.as_view(), name='delete_product'),
]