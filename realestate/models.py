from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/')
    description = models.TextField()


class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
