from rest_framework import routers
from django.urls import path
from .views import (
    UserViewSet,
    InterviewViewSet,
    TrackingViewSet,
    JobViewSet,
    ListingViewSet,
    OtpGenateView,
)


router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

router.register(r"jobs", JobViewSet)

router.register(r"interview", InterviewViewSet)

router.register(r"tracking", TrackingViewSet)
router.register(r"jobs-list", ListingViewSet)

urlpatterns = [
    path("otp/", OtpGenateView.as_view()),
]
urlpatterns += router.urls
