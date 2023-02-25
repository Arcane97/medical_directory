from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'refbooks', views.ReferenceBookListView)
router.register(r'refbooks/(?P<id>\d+)/elements', views.ReferenceBookElementListView, basename='refbooks-elements')

urlpatterns = [
    path('refbooks/<int:id>/check_element/', views.ElementValidationView.as_view(),
         name='element-validation'),
    *router.urls,
]
