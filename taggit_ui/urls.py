
from django.urls import re_path
from .views import DeleteTagAPI


urlpatterns = [
    re_path(r'^tagapi/delete/(?P<id>\d+)', DeleteTagAPI.as_view(), name='delete_tag_api'),
]
