# DJANGO PROJECT IMPORTS
from django.conf.urls import url, include
from django.contrib import admin

# THIRD PARTY LIBRARIES IMPORT
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    # Django Admin urls.
    url(r'^admin/', admin.site.urls),

    url(r'^docs/?', get_swagger_view(title='Reviews API Documentation')),
    url(r'^registration/', include('registration.urls')),
    url(r'^auth/', include('authentication.urls')),
    url(r'^reviews/', include('reviews.urls')),

]
