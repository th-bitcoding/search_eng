from django.contrib import admin
from django.urls import path, include
# from . import views
from rest_framework import routers
from .views import *

# router = routers.DefaultRouter()
# router.register(r'search', SearchengineViewSet)

urlpatterns = [
   # path('api/', include(router.urls)),
   path("api/search_value/", SearchengineAPIView.as_view()),
   path("api/deffer_sol/", DiffereSol.as_view()),
   # path("api/search_value/", MyModelSearchView.as_view()),

]