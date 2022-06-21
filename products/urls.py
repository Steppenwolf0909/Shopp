from django.urls import include, re_path, path
from . import views

urlpatterns = [
    path('all/', views.ListProductsAPIView.as_view(), name='get_products'),
    path('detail/<str:pk>/', views.DetailProductAPIView.as_view(), name='detail_products'),
    path('', views.SearchResultsView.as_view(), name='search_results'),
    path('filter/', views.FilterResultsView.as_view(), name='search_results'),
    path('get_favorite/', views.ListFavoriteAPIView.as_view(), name='get_favorite'),
    path('create_favorite/', views.CreateFavoriteAPIView.as_view(), name='create_favorite'),
    path('delete_favorite/', views.DeleteFavoriteAPIView.as_view(), name='delete_favorite'),
    path('create_product/', views.CreateProductAPIView.as_view(), name='create_product'),
    path('delete_product/<int:pk>/', views.DeleteProductAPIView.as_view(), name='delete_product'),
    path('update_product/<int:pk>/', views.UpdateProductAPIView.as_view(), name='delete_product'),
    path('get_asset_template/<int:category_id>/', views.GetAssetTemplate.as_view(), name='asset_template'),
    path('get_categories/', views.GetCategories.as_view(), name='get_categories'),
    path('add_photo/', views.AddPhotoAPIView.as_view(), name='add_photo'),
    path('delete_photo/<int:pk>/', views.DeletePhotoAPIView.as_view(), name='delete_photo'),

]