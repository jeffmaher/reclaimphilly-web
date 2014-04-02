from django.db import models
from hashlib import md5
import random

# Create your models here.
class Location(models.Model):
    """
    Represents a geographic location with the following properties:
    - latitude (required): Between -90 and 90
    - longitude (required): Between -180 and 180
    - lot_type (required): Either "bldg" or "lot"
    - address (optional): Stret address
    - description (optional): Description of the Location
    - picture (optional): An image of the Location
    """


    # Physical location data
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
    address = models.CharField(max_length=200, blank=True, null=True)

    # Valid types
    VALID_TYPES = ("nrs", "lot", "res")
    LOCATION_TYPES = ( # Keep this in-sync with VALID_TYPES
                       ("nrs", "Non-residential"),
                       ("lot", "Lot"),
                       ("res", "Residential")
    )
    lot_type = models.CharField(max_length="3", choices=LOCATION_TYPES)

    # Description
    description = models.CharField(max_length="200", blank=True, null=True)

    # Pictures
    # The size should be limited via the web server (to prevent massive uploads)
    # http://stackoverflow.com/a/6195637/249016
    def upload_to(instance, filename):
        new_filename = md5("%s/%s/%i" % (instance.address, filename, random.randint(1, 99999999))).hexdigest()
        return "images/locations/%s/%s.jpeg" % ("-".join(instance.address.lower().split()), new_filename)

    picture = models.ImageField(upload_to=upload_to, blank=True, null=True)

    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)

    def __unicode__(self):
        return "(" + str(self.id) + ") Latitude: " + str(self.latitude) + ", " + "Longitude: " + str(self.longitude)


class GeocodeCache(models.Model):
    address = models.CharField(max_length=200, blank=False, null=False)
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
