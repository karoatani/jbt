from rest_framework import serializers
from .models import User, Job, Interview, Tracking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "user",
            "title",
            "company_name",
            "application_date",
            "status",
            "notes",
        ]

    def create(self, validated_data):
        pk = self.context["request"].user.id
        user = User.objects.get(id=pk)
        validated_data["user"] = user
        return super().create(validated_data)


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ["id", "job", "interview_date"]


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ["id", "job", "created_at", "modiefied_date", "stages"]
