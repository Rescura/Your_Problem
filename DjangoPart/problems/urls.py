from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from problems.views import ProblemsViewSet, ReplyViewSet

router = routers.DefaultRouter()

# prefix = problems , viewset = MovieViewSet
router.register('problems', ProblemsViewSet)
urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^', include(router.urls)),
]