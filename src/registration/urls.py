# DJANGO LIBRARY IMPORT
from django.conf.urls import url
# PROJECT IMPORT
from .views import RegisterView


urlpatterns = [
    url(r'^$', RegisterView.as_view()),
]
