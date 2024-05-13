from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/')
    description = models.TextField()


class PropertyType(models.Model):
    property_type = models.CharField(max_length=50)

    def __str__(self):
        return self.property_type


class Neighborhood(models.Model):
    neighborhood = models.CharField(max_length=25)

    def __str__(self):
        return self.neighborhood


class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)

    property_type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING)
    price = models.IntegerField()
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.DO_NOTHING)
    featured = models.BooleanField(default=False)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    balcony = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=(
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Pending', 'Pending'),
    ))
    image1 = models.ImageField(upload_to='property_images/')
    image2 = models.ImageField(upload_to='property_images/')
    image3 = models.ImageField(upload_to='property_images/')
    image4 = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, null=True, blank=True)
    price_range = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_type} - {self.neighborhood} - {self.price_range}"
