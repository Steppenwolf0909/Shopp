from django.urls import include, re_path, path
from . import views

urlpatterns = [
    re_path('^', views.SearchResultsView.as_view(), name='search_results'),
    path('get_favorite/', views.ListFavoriteAPIView.as_view(), name='get_favorite'),
    path('create_favorite/', views.CreateFavoriteAPIView.as_view(), name='create_favorite'),
    path('delete_favorite/', views.DeleteFavoriteAPIView.as_view(), name='delete_favorite'),
]