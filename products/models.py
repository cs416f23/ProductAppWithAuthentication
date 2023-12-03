from django.db import models
from django.contrib.auth.models import User

# This is just a tuple defined to store 4 different PRODUCT_CATEGORY
# The user can be presented with these product categories
# When saving a product into the db we can use these options as product category
PRODUCT_CATEGORY = (
    ('Electronic', 'Electronic'),
    ('Dairy', 'Dairy'),
    ('Snack', 'Snack'),
    ('Other', 'Other'),
)


class Product(models.Model):
    # User model is created by Django. Instead of creating our own User model, we can simply use Django's user model.
    # the following line create a ForeignKey in your table
    # Since each user can have many products, 1-to-many relationship is needed.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20, blank=True, choices=PRODUCT_CATEGORY)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description
