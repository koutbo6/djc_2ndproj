from django.db import models
# Recommended way to get get
# the User Model
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

class ProductRatingManager(models.Manager):
    def products_with_score(self):
        return self.get_queryset().annotate(score=models.Avg("rating__score"))

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICE = (
        (u"car", _(u"Cars")),
        (u"swt", _(u"Sweets")),
        (u"gms", _(u"Games")),
        (u"jet", _(u"Jet Planes")),
    )


    # CharField holds a string
    # The first parameter is verbose_name
    # max_length is number of characters allowed
    name = models.CharField("product name", max_length=64, blank=False, )
    # blank is used whether the field can be blank or not
    # blank is false by default for all field types
    url = models.URLField("product page", blank=True)
    category = models.CharField(max_length=64, blank=True, choices=CATEGORY_CHOICE)
    # TextField holds a variable length field
    # usually used for large string based documents
    # use it for descriptions and when you do not
    # need to search the field
    description = models.TextField("product description",blank=True)
    # Product could have multiple users
    # Product can have no users
    # there is a problem here
    # how can we fix it?
    reviewers = models.ManyToManyField(get_user_model(), related_name='reviewed', through='Rating', blank=True, null=True)
    submitter = models.ForeignKey(get_user_model(), blank=True, null=True)

    objects = ProductRatingManager()

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.category)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('product_details', kwargs={"pid":str(self.id)})

    def get_rating_score(self):
        return self.rating_set.aggregate(avg_score=models.Avg("score")).values()[0] or "N/A"
        
class Rating(models.Model):
    # This established a one to many relationship between
    # Product (one) and Rating (Many)
    # other relations are OneToOne and ManyToMany
    product = models.ForeignKey(Product, verbose_name="reviewed product")
    # Float value that is 0.0 by default
    # null parameter means that we can store None value in DB
    # the null parameter is usefull in textbased fields
    # because empty list is always stored
    score = models.FloatField(default=0.0, blank=True, null=True,) #null is useless in text fields
    comment = models.TextField("product description",blank=True)
    # Store DimeTime in which review was created
    # auto_now_add means that the current datetime
    # is inserted when the object is first created
    # When auto_now_add is True then default and blank
    # are overridden to now and True
    created_at = models.DateTimeField("reviewed at", auto_now_add=True)
    # auto_now means update the field to now
    # everytime it is saved
    updated_at = models.DateTimeField("last updated", auto_now_add=True, auto_now=True)
    # rating is associated with a single user
    reviewer = models.ForeignKey(get_user_model())



class UserProfile(models.Model):
    # every user has a single profile
    user = models.OneToOneField(get_user_model())
    location = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)



