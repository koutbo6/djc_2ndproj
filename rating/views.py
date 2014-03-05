from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .models import  Product, Rating
from .forms import ProductForm, RatingForm
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory, inlineformset_factory, modelformset_factory

# Create your views here.
def product_list(request):
    # construct a queryset
    qs = Product.objects.products_with_score().select_related('submitter')
    return render(request, "rating/product_list.html", {"products":qs})

def product_details(request, pid):
    obj = get_object_or_404(Product, pk=pid)
    return render(
        request,
        "rating/product_detail.html",
        {"product": obj, },
    )

# multiple product entry
def product_list_entry(request):
    if not request.user.is_authenticated():
        # fetch an authenticated user (demo only)
        u = authenticate(username="foo", password="123")
        login(request, u)

    # this changed, param is model rather than form
    # everything else is the same
    ProductFormSet = modelformset_factory(Product, extra=0)
    
    if request.method == "POST":
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            [Product.objects.create(**x.cleaned_data) for x in formset]
            return redirect('product_list')
    else:
        # set submitter hidden field to logged in user
        # need just 2 forms
        initial = [{"submitter":request.user} for x in xrange(2)]
        formset = ProductFormSet(initial=initial)
        
    return render(
        request,
        "rating/product_list_entry.html",
        {
            "formset":formset,
        },
    )

def product_rate(request, pid):
    # login the user if he/she is not
    if not request.user.is_authenticated():
        # fetch an authenticated user
        u = authenticate(username="foo", password="123")
        login(request, u)
    product = get_object_or_404(Product, pk=pid)

    # only difference is here
    # no import for ModelForm needed
    # factory method creates the class
    # on the fly, everything else is the same
    NewRatingForm = modelform_factory(Rating)
    if request.method == "POST":
        form = NewRatingForm(request.POST)
        if form.is_valid():
            Rating.objects.create(**form.cleaned_data)
            return redirect(form.cleaned_data["product"])
    else:
        form = NewRatingForm(initial={"reviewer":request.user, "product":product})
    return render(
        request,
        "rating/product_rate.html",
        {"form": form, "product": product}
    )


def mass_edit_product_rate(request, pid):
    # login the user if he/she is not
    if not request.user.is_authenticated():
        # fetch an authenticated user
        u = authenticate(username="foo", password="123")
        login(request, u)
    product = get_object_or_404(Product, pk=pid)



    # create the InlineFormSet class on the fly
    MassRatingFormSet = inlineformset_factory(Product, 
        Rating, extra=3, can_delete=False)
    # everything else is almost the same
    if request.method == "POST":
        # slight difference is the instance param
        # this is used to specify the parent instance
        formset = MassRatingFormSet(request.POST, instance=product)
        if formset.is_valid():
            for item in formset:
                obj = item.cleaned_data.get("id")
                # update current object
                if obj:
                    for k,v in item.cleaned_data.items():
                        if hasattr(obj, k) and k != "id":
                            setattr(obj, k, v)
                    obj.save()
                else:
                    Rating.objects.create(**item.cleaned_data)
            
            return redirect('product_list')
    else:
        # Remember to set instance here as well
        # initial values will be populated correctly
        formset = MassRatingFormSet(instance=product)
        
    return render(
        request,
        "rating/product_list_entry.html",
        {
            "formset":formset,
        },
    )

def create_product(request):

    # login the user if he/she is not
    if not request.user.is_authenticated():
        # fetch an authenticated user
        u = authenticate(username="foo", password="123")
        login(request, u)

    # check for submission
    if request.method == "POST":
        # creating bounded form
        # request.POST is just a dict
        form = ProductForm(request.POST) 
        # validating
        if form.is_valid():
            # processing on success
            # p = Product.objects.create(
            #     name=form.cleaned_data["name"],
            #     url=form.cleaned_data.get("url"),
            #     submitter=form.cleaned_data.get("submitter"),
            # )
            # return redirect('product_list')

            # # or

            p = Product.objects.create(**form.cleaned_data)
            return redirect(p)
    else:
        form = ProductForm(
            initial={"submitter":request.user}
        )

    return render(
        request,
        "rating/product_create.html",
        {"form": form, }
    )

