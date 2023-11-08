from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class BaseUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")
        return super().create_user(
            username=username, email=email, password=password, **extra_fields
        )

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return super().create_superuser(
            username=username, email=email, password=password, **extra_fields
        )


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    username_validator = UnicodeUsernameValidator
    objects = BaseUserManager()
    email = models.EmailField(_("email address"), blank=True, unique=True, null=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        default="",
    )


STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("ACCEPTED", "Accepted"),
    ("REJECTED", "Rejected"),
)
STAGES_CHOICES = (
    ("SUBMITTED", "Submitted"),
    ("SCHEDULED", "Scheduled"),
    ("RECEIVED", "Received"),
)


class Job(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    company_name = models.CharField(max_length=255)

    application_date = models.DateField()

    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="PENDING")
    notes = models.TextField()


class Interview(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    interview_date = models.DateTimeField()


class Tracking(models.Model):
    job = models.ForeignKey(
        "Job", on_delete=models.SET_NULL, null=True, related_name="tracking"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modiefied_date = models.DateTimeField(auto_now=True)
    stages = models.CharField(max_length=9, choices=STAGES_CHOICES, default="SUBMITTED")
