from django.core.exceptions import ValidationError

def validate_product_is_active(value):
    if not value.active:
        raise ValidationError(
            '{product} product is not active.'.format(product=value)
        )
