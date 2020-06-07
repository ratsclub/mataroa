from django.core import validators
from django.core.exceptions import ValidationError


class StrictUsernameValidator(validators.RegexValidator):
    regex = r"^[a-z\d-]+\Z"
    message = "Enter a valid username, it should include only lowercase letters, numbers, and -"
    flags = 0


def validate_domain_name(value):
    if "." not in value:
        raise ValidationError("Invalid domain name")