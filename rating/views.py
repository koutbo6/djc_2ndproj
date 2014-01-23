from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .models import  Product, Rating
from .forms import ProductForm, RatingForm
from django.forms.formsets import formset_factory

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

def product_list_entry(request):
    if not request.user.is_authenticated():
        # fetch an authenticated user (demo only)
        u = authenticate(username="foo", password="123")
        login(request, u)

    ProductFormSet = formset_factory(ProductForm, extra=0)
    
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
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.create(**form.cleaned_data)
            return redirect(form.cleaned_data["product"])
    else:
        form = RatingForm(initial={"reviewer":request.user, "product":product})
    return render(
        request,
        "rating/product_rate.html",
        {"form": form, "product": product}
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

