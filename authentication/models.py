from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone


from .constants import DEFAULT_ROLES


class CustomUserManager(UserManager):
    """custom user manager"""

    def _create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise ValueError("Email field is required.")
        if password is None:
            raise ValueError("Password field is required.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        role_id = DEFAULT_ROLES["admin"]
        role_name = "admin"
        extra_fields["role"] = get_or_create_role(role_id, role_name)

        return self._create_user(
            username=email, email=email, password=password, **extra_fields
        )


class Role(models.Model):
    """user's Role which is used for giving permissions"""

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def get_or_create_role(role_id, role_name):
    role, created = Role.objects.get_or_create(id=role_id, defaults={"name": role_name})
    return role


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    """This is my custom User model"""

    zoho_id = models.PositiveBigIntegerField(unique=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    age = models.PositiveSmallIntegerField(null=True, default=2)
    phone = models.CharField(
        ("phone"), max_length=15, unique=True, null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    beruf = models.CharField(
        max_length=30,
        choices=[("Elektriker", "Elektriker"), ("Vertrieb", "Vertrieb")],
        null=True,
        default=None,
    )
    users_aufschlag = models.PositiveSmallIntegerField(null=False, default=0)
    typ = models.CharField(
        max_length=255,
        choices=[
            ("keine", "keine"),
            ("Evolti", "Evolti"),
            ("Vertrieb", "Vertrieb"),
            ("Freelancer", "Freelancer"),
        ],
        null=True,
        default=None,
    )
    kuerzel = models.CharField(max_length=3, null=True, unique=True)
    gerat = models.CharField(max_length=30, null=True, blank=True, unique=False)
    is_active = models.BooleanField(default=True)
    imei = models.BigIntegerField(null=True, blank=True, unique=True)
    anbieter = models.CharField(max_length=30, null=True, blank=True, unique=False)
    google_account = models.EmailField(null=True, blank=True, unique=True)
    google_passwort = models.CharField(
        max_length=30, null=True, blank=True, unique=False
    )
    sim_pin = models.SmallIntegerField(null=True, blank=True, unique=False)
    is_superuser = models.BooleanField(default=False)
    zoho_data = models.JSONField(default=dict, blank=True)
    zoho_data_text = models.TextField(default="", blank=True)
    sonstiges = models.TextField(blank=True, null=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date_joined = models.DateTimeField(("date joined"), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"

    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    class Meta:
        # db_table = "users"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    @receiver(post_migrate)
    def create_default_roles(sender, **kwargs):
        for role_name, role_id in DEFAULT_ROLES.items():
            get_or_create_role(role_id, role_name)
