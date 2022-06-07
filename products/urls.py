from django.urls import include, re_path
from products.views import SearchResultsView

urlpatterns = [
    re_path('^', SearchResultsView.as_view(), name='search_results'),
]