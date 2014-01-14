from django.db import models

# Create your models here.
class Product(models.Model):
    # CharField holds a string
    # The first parameter is verbose_name
    # max_length is number of characters allowed
    name = models.CharField("product name", max_length=64)
    # blank is used whether the field can be blank or not
    # blank is false by default for all field types
    url = models.URLField("product page", blank=True)
    category = models.CharField(max_length=64, blank=True)
    # TextField holds a variable length field
    # usually used for large string based documents
    # use it for descriptions and when you do not
    # need to search the field
    description = models.TextField("product description",blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.category)

class Rating(models.Model):
    # This established a one to many relationship between
    # Product (one) and Rating (Many)
    # other relations are OneToOne and ManyToMany
    product = models.ForeignKey(Product, verbose_name="reviewed product")
    # Float value that is 0.0 by default
    # null parameter means that we can store None value in DB
    # the null parameter is usefull in textbased fields
    # because empty list is always stored
    score = models.FloatField(default=0.0, blank=True, null=True) #null is useless in text fields
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
