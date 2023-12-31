# urls.py

from django.urls import path
from .views import ElementListCreateView
from .views import ImageListView, ElementDetailView, UniqueValuesView, SimilarElementsView, ElementDetailViewByURL

urlpatterns = [
    path('elemente/', ElementListCreateView.as_view(), name='element-list-create'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('elements/<int:element_id>/', ElementDetailView.as_view(), name='element-detail'),
    path('elements-by-url/', ElementDetailViewByURL.as_view(), name='element-detail-by-url'),  # Adaugă această linie
    path('unique-values/', UniqueValuesView.as_view(), name='unique-values'),
    path('similar-elements/<int:element_id>/', SimilarElementsView.as_view(), name='similar-elements'),
]

