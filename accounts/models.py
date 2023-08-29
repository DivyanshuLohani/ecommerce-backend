from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from shortuuidfield import ShortUUIDField
from django.core.validators import RegexValidator
from base.models import BaseModel

AUTH_PROVIDER = (
    ('email', 'Email'),
    ('google', 'Google'),
    ('facebook', 'facebook')
)

PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


# Create your models here.
class NewUserManager(UserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=email
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)


class User(AbstractUser, BaseModel):

    uid = ShortUUIDField(max_length=14, auto=True)

    auth_provider = models.CharField(
        choices=AUTH_PROVIDER,
        default=AUTH_PROVIDER[0][0],
        max_length=30
    )

    email = models.EmailField(unique=True)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Address(BaseModel):
    uid = ShortUUIDField(max_length=14, auto=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=256)
    contact = models.CharField(validators=[PHONE_REGEX], max_length=17)
    postal_code = models.CharField(
        max_length=6,
        validators=[RegexValidator('^[0-9]{6}$', ('Invalid postal code'))],
    )
    flat_name = models.CharField(max_length=32, default="")
    area = models.CharField(max_length=128)
    landmark = models.CharField(max_length=64, default="")
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)

    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.flat_name}, {self.area}, {self.city}, {self.country} {self.postal_code}"


def vendor_upload(instance, filename):
    ext = filename.split(".")[-1]

    return f"media/users/{instance.user.id}/{hash(instance.id)}.{ext}"


class Vendor(BaseModel):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="vendor"
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=4096)
    banner_image = models.ImageField(
        upload_to=vendor_upload,
        null=True,
        default=None,
        blank=True
    )
    address = models.CharField(max_length=1024)
    contact = models.CharField(validators=[PHONE_REGEX], max_length=17)

    def __str__(self) -> str:
        return self.name
