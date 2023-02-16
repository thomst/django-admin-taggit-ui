
from django.urls import path
from .views import RemoveTagApi


urlpatterns = [
    path('remove-tag/<int:tag_id>/from/<slug:app_label>/<slug:model_name>/', RemoveTagApi.as_view(), name='remove-tag'),
]
