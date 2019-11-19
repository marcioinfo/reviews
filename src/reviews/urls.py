# DJANGO LIBRARY IMPORT
from django.conf.urls import url
# PROJECT IMPORT
from reviews.views import ReviewView


urlpatterns = [
    url(r'^$', ReviewView.as_view()),
]
