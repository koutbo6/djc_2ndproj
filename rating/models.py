from django.conf import settings  # add this
from django.db import models


class ProductRatingManager(models.Manager):

    def products_with_score(self):
        return self.get_queryset().annotate(score=models.Avg("rating__score"))


class Product(models.Model):
    CATEGORY_CHOICE = (
        (u"car", u"Cars"),
        (u"swt", u"Sweets"),
        (u"gms", u"Games"),
        (u"jet", u"Jet Planes"),
    )

    # CharField holds a string
    # The first parameter is verbose_name
    # max_length is number of characters allowed
    name = models.CharField("product name", max_length=64, blank=False, )
    # blank is used whether the field can be blank or not
    # blank is false by default for all field types
    url = models.URLField("product page", blank=True)
    category = models.CharField(
        max_length=64, blank=True, choices=CATEGORY_CHOICE)
    # TextField holds a variable length field
    # usually used for large string based documents
    # use it for descriptions and when you do not
    # need to search the field
    description = models.TextField("product description", blank=True)
    # Product could have multiple users
    # Product can have no users
    # there is a problem here
    # how can we fix it?
    reviewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='reviewed', through='Rating',
        blank=True, null=True)
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)

    objects = ProductRatingManager()

    def __str__(self):
        return "{} ({})".format(self.name, self.category)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('product_details', kwargs={"pid": str(self.id)})

    def get_rating_score(self):
        return self.rating_set.aggregate(
            avg_score=models.Avg("score")).get("avg_score") or "N/A"


class Rating(models.Model):
    # This established a one to many relationship between
    # Product (one) and Rating (Many)
    # other relations are OneToOne and ManyToMany
    product = models.ForeignKey(Product, verbose_name="reviewed product")
    # Float value that is 0.0 by default
    # null parameter means that we can store None value in DB
    # the null parameter is usefull in textbased fields
    # because empty list is always stored
    # null is useless in text fields
    score = models.FloatField(default=0.0, blank=True, null=True,)
    comment = models.TextField(blank=True)
    # Store DimeTime in which review was created
    # auto_now_add means that the current datetime
    # is inserted when the object is first created
    # When auto_now_add is True then default and blank
    # are overridden to now and True
    created_at = models.DateTimeField("reviewed at", auto_now_add=True)
    # auto_now means update the field to now
    # everytime it is saved
    updated_at = models.DateTimeField(
        "last updated", auto_now_add=True, auto_now=True)
    # rating is associated with a single user
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL)


class UserProfile(models.Model):
    # every user has a single profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    location = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
