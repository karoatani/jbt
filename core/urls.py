from rest_framework import routers
from .views import UserViewSet, InterviewViewSet, TrackingViewSet, JobViewSet


router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

router.register(r"jobs", JobViewSet)

router.register(r"interview", InterviewViewSet)

router.register(r"tracking", TrackingViewSet)
urlpatterns = router.urls
