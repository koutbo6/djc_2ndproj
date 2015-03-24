from django.shortcuts import render, redirect, get_object_or_404
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required

from .models import Product, Rating
from .forms import ProductForm, RatingForm


def product_list(request):
    # construct a queryset
    qs = Product.objects.all()
    return render(request, "rating/product_list.html", {"products": qs})


def product_details(request, pid):
    obj = get_object_or_404(Product, pk=pid)
    return render(
        request,
        "rating/product_detail.html",
        {"product": obj, },
    )


@login_required
def create_product(request):
    # check for submission
    if request.method == "POST":
        # creating bounded form
        # request.POST is just a dict
        form = ProductForm(request.POST)
        # validating
        if form.is_valid():
            # processing on success (long method)
            # p = Product.objects.create(
            #     name=form.cleaned_data["name"],
            #     url=form.cleaned_data.get("url"),
            #     submitter=form.cleaned_data.get("submitter"),
            # )
            # return redirect('product_list')

            # or short method
            p = form.save()
            # redirect to product details for item we created
            return redirect('product_details', pid=p.id)
    else:
        form = ProductForm(
            initial={"submitter": request.user}
        )

    return render(
        request,
        "rating/product_create.html",
        {"form": form, }
    )


@login_required
def product_rate(request, pid):
    # let's fetch the product object
    product = get_object_or_404(Product, pk=pid)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            # the product details view function looks like this
            # def product_details(request, pid):
            return redirect('product_details', pid=product.id)
    else:
        form = RatingForm(
            initial={"reviewer": request.user, "product": product})
    return render(
        request,
        "rating/product_rate.html",
        {"form": form, "product": product}
    )


# some advanced stuff we didnt talk about
# try to read the code and find out what is happening
def product_list_entry(request):
    ProductFormSet = formset_factory(ProductForm, extra=0)

    if request.method == "POST":
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            # run save on every item in formset list
            [x.save() for x in formset]
            return redirect('product_list')
    else:
        # set submitter hidden field to logged in user
        # need just 2 forms
        initial = [{"submitter": request.user} for x in range(2)]
        formset = ProductFormSet(initial=initial)

    return render(
        request,
        "rating/product_list_entry.html",
        {
            "formset": formset,
        },
    )


def advanced_product_list(request):
    # construct a queryset
    qs = Product.objects.products_with_score()
    return render(request, "rating/product_list.html", {"products": qs})
