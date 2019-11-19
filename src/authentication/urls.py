# DJANGO LIBRARY IMPORTS
from django.conf.urls import url
# PROJECT IMPORTS
from authentication import views


urlpatterns = [
    url(r'^login', views.LogInView.as_view()),
    url(r'logout', views.LogOutView.as_view()),
]
