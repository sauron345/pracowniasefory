from django.core.exceptions import ValidationError
import os


def allow_only_images(value):
    extension = os.path.splitext(value.name)[1]
    print(extension)

    valid_extensions = ['.jpg', '.jpeg', '.png']

    if extension.lower() not in valid_extensions:
        raise ValidationError(
            "Unsupported file extension. Allowed only extensions: " + str(valid_extensions)
        )
