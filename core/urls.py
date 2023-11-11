from rest_framework import routers
from django.urls import path
from .views import (
    UserViewSet,
    InterviewViewSet,
    TrackingViewSet,
    JobViewSet,
    OtpGenateView,
)


router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

router.register(r"jobs", JobViewSet)

router.register(r"interview", InterviewViewSet)

router.register(r"tracking", TrackingViewSet)

urlpatterns = [
    path("otp/", OtpGenateView.as_view()),
]
urlpatterns += router.urls
