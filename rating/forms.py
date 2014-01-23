from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Product

def validate_rating(value):
    if 0 > value or value > 5.0:
        raise ValidationError(u'%s is not between 0 and 5.0' % value)

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=64,
#         label=u'Product name')
#     # ProductForm in forms.py
#     url = forms.URLField(max_length=200, 
#         required=False, label=u'Product page',
#         widget=forms.URLInput,
#         )
#     category = forms.ChoiceField( 
#         required=False, label=u'Category',
#         choices=Product.CATEGORY_CHOICE,
#         )
#     description = forms.CharField(required=False, 
#         label=u'Product description',
#         widget=forms.Textarea,
#         )
#     submitter = forms.ModelChoiceField(
#         queryset=get_user_model().objects.all(),
#         required=False, label=u'Submitter',
#         widget=forms.HiddenInput
#         )


class ProductForm(forms.ModelForm):

    #overriding submitter to use HiddenInput
    submitter = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False, label=u'Submitter',
        widget=forms.HiddenInput
        )    

    class Meta:
        model = Product
        # This is how you include 3 fields only
        # without it all fields are in
        # we exclude reviewers
        # avoid using exclude option!
        fields = ['name', 'url', 'category', 
            'description', 'submitter']


    # reviewers = forms.ModelMultipleChoiceField(
    #     queryset=get_user_model().objects.all(),
    #     required=False, label=u'Reviewers')

class RatingForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label=u'Reviewed product', 
        widget=forms.HiddenInput)
    score = forms.FloatField(
        required=False, 
        initial=0.0,
        label=u'Score',
        validators=[validate_rating],
        )
    comment = forms.CharField(
        required=False,
        label=u'Product description')
    reviewer = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        label=u'Reviewer', 
        widget=forms.HiddenInput)