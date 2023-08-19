from django.db import models
from django.utils.timezone import now


class Property(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = "For Sale"
        FOR_RENT = "For Rent"

    class PropertyType(models.TextChoices):
        HOUSE = "House"
        APARTMENT = "Apartment"
        LAND = "Land"

    agent = models.EmailField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sale_type = models.CharField(
        max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE
    )
    property_type = models.CharField(
        max_length=10, choices=PropertyType.choices, default=PropertyType.HOUSE
    )
    main_photo = models.ImageField(upload_to="property_service/")
    photo_1 = models.ImageField(upload_to="property_service/")
    photo_2 = models.ImageField(upload_to="property_service/")
    photo_3 = models.ImageField(upload_to="property_service/")
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
