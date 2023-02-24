from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'refbooks', views.ReferenceBookListView)
router.register(r'refbooks/(?P<id>\d+)/elements', views.ReferenceBookElementListView)

urlpatterns = router.urls
