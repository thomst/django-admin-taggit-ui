from django.conf.urls import url
from .views import DeleteTagAPI


urlpatterns = [
    url(r'^tagapi/delete/(?P<id>\d+)', DeleteTagAPI.as_view(), name='delete_tag_api'),
]
