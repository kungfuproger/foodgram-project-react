from django.core.validators import MinValueValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy


@deconstructible
class RuMinValueValidator(MinValueValidator):
    message = gettext_lazy(
        "Убедитесь, что это значение больше либо равно %(limit_value)s."
    )
