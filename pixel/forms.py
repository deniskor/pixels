from django import forms
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

WIDTH = 20
HEIGHT = 20


class PixelForm(forms.Form):
    x = forms.IntegerField(required=True, validators=[MaxValueValidator(WIDTH), MinValueValidator(1)])
    y = forms.IntegerField(required=True, validators=[MaxValueValidator(HEIGHT), MinValueValidator(1)])


class PixelPOSTForm(PixelForm):
    color = forms.CharField(max_length=6, required=True,
                            validators=[RegexValidator(r'^[0-9a-fA-F]{6}$')])
