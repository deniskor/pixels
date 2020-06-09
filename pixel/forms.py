from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Pixel


class PixelForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        rect = cleaned_data.get("rect")

        if not rect:
            raise ValidationError('invalid rectangle')

        x = cleaned_data.get("x")
        y = cleaned_data.get("y")

        if not (0 < x <= rect.width) or not (0 < y <= rect.height):
            raise ValidationError('invalid coords')

        return cleaned_data

    class Meta:
        model = Pixel
        exclude = ['color']


class PixelPOSTForm(PixelForm):
    color = forms.CharField(max_length=6, required=True,
                            validators=[RegexValidator(r'^[0-9a-fA-F]{6}$')])
