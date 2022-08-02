from django.urls import path

from . import views

urlpatterns = [
    path('products/<int:pk>/', views.GetUserProductsView.as_view(), name='get_user'),
    path('user/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),
    path('user/', views.UpdateUserView.as_view(), name='users_list'),
    path('review/', views.CreateReviewView.as_view(), name='create_review')
]
