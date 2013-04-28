from django.db import models

# Create your models here.
class Location(models.Model):
    """
    Represents a geographic location with the following properties:
    - latitude (required): Between -90 and 90
    - longitude (required): Between -180 and 180
    - type (required): Either "bldg" or "lot"
    - address (optional): Stret address
    - description (optional): Description of the Location
    - picture (optional): An image of the Location
    """


    # Physical location data
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
    address = models.CharField(max_length=200, blank=True, null=True)

    # Valid types
    VALID_TYPES = ("com", "lot", "res")
    LOCATION_TYPES = ( # Keep this in-sync with VALID_TYPES
                       ("com", "Commercial"),
                       ("lot", "Lot"),
                       ("res", "Residential")
    )
    type = models.CharField(max_length="3", choices=LOCATION_TYPES)

    # Description
    description = models.CharField(max_length="200", blank=True, null=True)

    # Picture
    # The size should be limited via the web server (to prevent massive uploads)
    # http://stackoverflow.com/a/6195637/249016
    picture = models.ImageField(upload_to="images/locations", blank=True, null=True)

    def __unicode__(self):
        return "(" + str(self.id) + ") Latitude: " + str(self.latitude) + ", " + "Longitude: " + str(self.longitude);


class GeocodeCache(models.Model):
    address = models.CharField(max_length=200, blank=False, null=False)
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)