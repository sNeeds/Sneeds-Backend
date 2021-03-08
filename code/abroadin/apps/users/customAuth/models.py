from phonenumber_field.modelfields import PhoneNumberField

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, is_email_verified, receive_marketing_email, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            is_email_verified=is_email_verified,
            receive_marketing_email=receive_marketing_email,
            last_login=now,
            date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(
            email, password, False, False, False, extra_fields.pop('receive_marketing_email', False),
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email, password, True, True, True, False, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    class UserTypeChoices(models.TextChoices):
        STUDENT = "Student"
        ADMIN = "Admin"  # For automatic chat and ...

    class AuthProviderTypeChoices(models.TextChoices):
        EMAIL = "Email"
        GOOGLE = "Google"
        FACEBOOK = "Facebook"

    email = models.EmailField(_('email address'), unique=True, max_length=256)
    phone_number = PhoneNumberField(null=True, blank=True)
    first_name = models.CharField(_('first name'), null=True, max_length=128, blank=True)
    last_name = models.CharField(_('last name'), null=True, max_length=128, blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False,
        choices=AuthProviderTypeChoices.choices,
        default=AuthProviderTypeChoices.EMAIL
    )
    user_type = models.CharField(
        max_length=128,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.STUDENT,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_email_verified = models.BooleanField(
        _('email verification status'),
        default=False,
        help_text=_('Designates whether the user email is verified.'),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False)
    date_last_action = models.DateTimeField(_('last action'), null=True, blank=True, editable=False)

    receive_marketing_email = models.BooleanField(
        _('receive marketing email status'),
        default=False,
        help_text=_('Designates whether the user wants to get marketing emails or news.'),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email)
        self.email = self.email.lower()

        super().save(*args, **kwargs)

    def update_date_last_action(self):
        self.date_last_action = timezone.now()
        self.save()

    def is_student(self):
        if self.user_type == self.UserTypeChoices.STUDENT:
            return True
        return False

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_pretty_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between in pretty format.
        """
        params = []
        if self.first_name is not None:
            params.append(str(self.first_name))
        if self.last_name is not None:
            params.append(str(self.last_name))
        full_name = ' '.join(params)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_instance(self, instance, **kwargs):
        for (key, value) in kwargs.items():
            setattr(instance, key, value)
        instance.save()


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
