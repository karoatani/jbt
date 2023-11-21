from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import (
    UserSerializer,
    JobSerializer,
    InterviewSerializer,
    TrackingSerializer,
    ListingSerializer,
)
from .models import User, Job, Interview, Tracking, Listing
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .utils import generate
from datetime import datetime, timedelta
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

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


# Otp verification Endpoint
class OtpGenateView(APIView):
    def get(self, request):
        otp = generate(60)
        request.session["otp"] = otp.now()
        request.session["expiry_date"] = (
            datetime.now() + timedelta(minutes=1)
        ).isoformat()
        return Response({"otp": request.session["otp"]}, status=HTTP_200_OK)

    def post(self, request):
        code = request.data.get("otp")

        print(request.session["otp"] == code)
        print(code)
        if datetime.now() < datetime.fromisoformat(request.session["expiry_date"]):
            if request.session["otp"] == code:
                return Response({}, status=HTTP_200_OK)
        return Response({"error": "invalid otp"}, status=HTTP_204_NO_CONTENT)


# job board integration


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]


# notification system
# monitoring tools

# sending and receiving mail
