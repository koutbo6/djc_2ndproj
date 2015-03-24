from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Product, Rating


def validate_rating(value):
    if 0 > value or value > 5.0:
        raise ValidationError(u'%s is not between 0 and 5.0' % value)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        widgets = {
            'submitter': forms.HiddenInput(),
            
        }
        # we are hiding revieweres field
        fields = ['name', 'url', 'category', 'description']


class RatingForm(forms.ModelForm):

    # to change validator (advanced)
    # we need to override the field definition
    # This will make sure the value for the score is between 0 and 5
    # see the function validate_rating
    score = score = forms.FloatField(
        required=False,
        initial=0.0,
        validators=[validate_rating, ],  # setting validator function
    )

    class Meta:
        model = Rating
        widgets = {
            'product': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
