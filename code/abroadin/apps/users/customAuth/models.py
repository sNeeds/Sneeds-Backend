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

    def get_admin_consultant_or_none(self):
        try:
            return self.get(user_type=CustomUser.UserTypeChoices.ADMIN_CONSULTANT)
        except CustomUser.DoesNotExist:
            return None


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    class UserTypeChoices(models.TextChoices):
        STUDENT = "Student"
        CONSULTANT = "Consultant"
        ADMIN_CONSULTANT = "Admin consultant"  # For automatic chat and ...

    email = models.EmailField(_('email address'), unique=True, max_length=256)
    phone_number = PhoneNumberField(null=True, blank=True)
    first_name = models.CharField(_('first name'), null=True, max_length=30, blank=True)
    last_name = models.CharField(_('last name'), null=True, max_length=150, blank=True)

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

    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        from abroadin.apps.users.consultants.models import ConsultantProfile

        super().clean()

        if self.user_type == self.UserTypeChoices.ADMIN_CONSULTANT:
            if CustomUser.objects.filter(user_type=CustomUser.UserTypeChoices.ADMIN_CONSULTANT).exclude(
                    id=self.id).exists():
                raise ValidationError("User with admin_consultant type exists.")
            if not ConsultantProfile.objects.filter(user__id=self.id).exists():
                raise ValidationError("No consultant profile for user with admin_consultant exists.")

    def save(self, *args, **kwargs):
        self.user_type = self.compute_user_type()

        self.email = self.__class__.objects.normalize_email(self.email)
        self.email = self.email.lower()

        super().save(*args, **kwargs)

    def update_date_last_action(self):
        self.date_last_action = timezone.now()
        self.save()

    def compute_user_type(self):
        from abroadin.apps.users.consultants.models import ConsultantProfile
        if self.user_type == self.UserTypeChoices.ADMIN_CONSULTANT:
            return
        elif ConsultantProfile.objects.filter(user__id=self.id).exists():
            return self.UserTypeChoices.CONSULTANT
        else:
            return self.UserTypeChoices.STUDENT

    def is_consultant(self):
        if self.user_type == self.UserTypeChoices.CONSULTANT:
            return True
        return False

    def is_student(self):
        if self.user_type == self.UserTypeChoices.STUDENT:
            return True
        return False

    def is_admin_consultant(self):
        if self.user_type == self.UserTypeChoices.ADMIN_CONSULTANT:
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

    # TODO: Move to ModelAdmin and change export_as_csv IMPORTANT - Bad design
    def has_form(self):
        from abroadin.apps.estimation.form.models import StudentDetailedInfo
        return StudentDetailedInfo.objects.filter(user__id=self.id).exists()

    # TODO: Move to ModelAdmin and change export_as_csv IMPORTANT - Bad design
    def home_university(self):
        from abroadin.apps.estimation.form.models import StudentDetailedInfo

        try:
            form = StudentDetailedInfo.objects.get(user__id=self.id)
        except StudentDetailedInfo.DoesNotExist:
            return None

        university_through_qs = form.university_through_qs()
        if not university_through_qs.exists():
            return None

        last_grade = university_through_qs.order_by_grade().last()

        return last_grade.university


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
