from django.utils.translation import gettext as _

import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.serializerfields import PhoneNumberField

from abroadin.apps.users.consultants.serializers import ShortConsultantProfileSerializer
from abroadin.apps.users.consultants.models import ConsultantProfile

from .utils import create_doi_contact

User = get_user_model()


def validate_user_password(password):
    try:
        # validate the password and catch the exception
        validators.validate_password(password)

    # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(e.messages)


def validate_email(email):
    qs = User.objects.filter(email__iexact=email)
    if qs.exists():
        raise serializers.ValidationError(_("User with this email already exists"))


def validate_phone_number(phone):
    try:
        int(phone)
    except (ValueError, TypeError):
        raise serializers.ValidationError(_("Phone number should be number only"))


class UserRegisterSerializer(serializers.ModelSerializer):
    token_response = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'phone_number',
            'token_response',
            'receive_marketing_email',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True},
            'receive_marketing_email': {'required': True}
        }

    def get_token_response(self, obj):
        data = {}
        refresh = RefreshToken.for_user(obj)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    def validate_password(self, value):
        validate_user_password(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value.lower()

    def validate_phone_number(self, value):
        validate_phone_number(value)
        return value

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            receive_marketing_email=validated_data.get('receive_marketing_email'),
            user_type=1,  # Only student can register with serializer
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            'first_name': {'required': False, 'read_only': True},
            'last_name': {'required': False, 'read_only': True},
            'id': {'required': False, 'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'is_email_verified',
            'receive_marketing_email',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'password': {'write_only': True, 'required': False},
            'is_email_verified': {'read_only': True, 'required': False},
            'receive_marketing_email': {'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)

        try:
            password = validated_data.pop('password')
        except:
            pass

        User().update_instance(instance, **validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class SafeUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            'id',
            'first_name',
            'last_name',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': False},
        }


class MyAccountSerializer(UserSerializer):
    consultant = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['user_type', 'consultant', ]

    def get_consultant(self, obj):
        try:
            consultant = ConsultantProfile.objects.get(user=obj)
            return ShortConsultantProfileSerializer(consultant, context={"request": self.context.get('request')}).data
        except ConsultantProfile.DoesNotExist:
            return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        attrs[self.username_field] = attrs[self.username_field].lower()

        try:
            user = User.objects.get(email=attrs[self.username_field])
            if not user.check_password(attrs['password']):
                raise AuthenticationFailed({"detail": "Password is incorrect."})

        except User.DoesNotExist:
            raise AuthenticationFailed({"detail": "No user found with this email."})

        data = super().validate(attrs)
        return data


class SubscribeSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=256,
        required=False,
    )

    phone_number = PhoneNumberField(
        required=False
    )

    first_name = serializers.CharField(
        max_length=256,
        required=False,
    )

    last_name = serializers.CharField(
        max_length=256,
        required=False,
    )

    class Meta:
        fields = [
            'email', 'phone_number'
        ]

        extra_kwargs = {
        }

    def validate_email(self, value):
        validate_email(value)
        return value.lower()

    # def validate_phone_number(self, value):
    #     validate_phone_number(value)
    #     return value

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise ValidationError(_('User must enter at least Email or Phone number for subscription.'))
        if attrs.get('email') is None:
            raise ValidationError(_('User must enter Email for subscription.'))
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        create_doi_contact.delay(validated_data.get('email'), str(validated_data.get('phone_number')),
                                 receive_marketing_email=True,
                                 first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'))
        return None

    def save(self, **kwargs):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)

        return self.instance