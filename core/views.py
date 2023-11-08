from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import (
    UserSerializer,
    JobSerializer,
    InterviewSerializer,
    TrackingSerializer,
)
from .models import User, Job, Interview, Tracking
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

# Create your views here.


# crud
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.is_superuser or request.user.id == instance.user.id:
            return Response(serializer.data)
        raise PermissionDenied

    def update(self, request, *args, **kwargs):
        pk = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == pk:
            return super().update(request, *args, **kwargs)

        raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == pk:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.is_superuser or request.user.id == instance.user.id:
            return Response(serializer.data)
        raise PermissionDenied

    def update(self, request, *args, **kwargs):
        pk = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == pk:
            return super().update(request, *args, **kwargs)

        raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == pk:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied


class TrackingViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingSerializer
    queryset = Tracking.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.is_superuser or request.user.id == instance.user.id:
            return Response(serializer.data)
        raise PermissionDenied

    def update(self, request, *args, **kwargs):
        pk = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == pk:
            return super().update(request, *args, **kwargs)

        raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == pk:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied
