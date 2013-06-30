import requests

from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404, HttpResponseBadRequest, \
    HttpRequest, HttpResponseServerError, HttpResponseNotAllowed
from django.conf import settings
from reclaimcities.apps.web.models import GeocodeCache


try:
    import simplejson as json
except ImportError:
    import json
from reclaimcities.libs.services import LocationService, UserService
import reclaimcities.libs.conversions as conversions
import re
from reclaimcities.apps.web.models import Location
from django.views.decorators.csrf import csrf_exempt


#
# TODO Move more of the validation into the service classes (or take a look at the forms libraries within django)
#

# Static / Class level helper objects
LOCATION_SERVICE = LocationService()
USER_SERVICE = UserService()
VALID_LOCATION_ID_REGEX = re.compile('^\d+$')
VALID_ADDRESS_REGEX = re.compile('^(\w|\.|\s|-)+$')
VALID_DESCRIPTION_REGEX = re.compile('^(\w|\.|\s|-|!|\?|\')+$')

def json_response(response_obj):
    """
    TODO document
    :param response_obj:
    :return:
    """
    response = []
    if response_obj:
        response = json.dumps(response_obj)
    else:
        response = json.dumps(response)
    return HttpResponse(response, mimetype='application/json', content_type='application/json; charset=utf8')


@csrf_exempt
def get_locations_in_radius(request): # , latitude, longitude, radius=0
    """
    TODO pydoc this better
    Gets a list of locations_dict within a given mile radius.

    Returned, is a GeoJSON array of Points with the following properties
    - id
    - address
    - picture (URL)
    - description
    - type   TODO plusjeff This is coming back as the DB string, not the descriptive English version -- change that

    Example Request:
    http://localhost:8000/services/locations?latitude=1&longitude=2&radius=3
    GET Params
        - latitude - number
        - longitude - number
        - radius - number
    """
    # Validate request - must be GET
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Validate latitude - required, number only
    try:
        latitude = request.GET['latitude']
        latitude = float(latitude)
    except KeyError:
        return HttpResponseBadRequest('Missing latitude parameter')
    except ValueError:
        return HttpResponseBadRequest('Non-numeric latitude parameter')

    # Validate longitude - required number only
    try:
        longitude = request.GET['longitude']
        longitude = float(longitude)
    except KeyError:
        return HttpResponseBadRequest('Missing longitude parameter')
    except ValueError:
        return HttpResponseBadRequest('Non-numeric longitude parameter')

    # Validate radius - required, number only
    try:
        radius = request.GET['radius']
        radius = float(radius)
    except KeyError:
        return HttpResponseBadRequest('Missing radius parameter')
    except ValueError:
        return HttpResponseBadRequest('Non-numeric radius parameter')

    # Perform search
    locations_dict = LOCATION_SERVICE.get_locations(latitude, longitude, radius)
    points = conversions.locations_to_points(locations_dict)

    return json_response(points)

@csrf_exempt
def get_location_by_id(request, id):
    """
    TODO pydoc this better
    Gets a single Location by its database ID column

    Returned, is a GeoJSON Point object with the following properties
    - id
    - address
    - picture (URL)
    - description
    - type   TODO This is coming back as the DB string, not the descriptive English version -- change that

    Sample request:
    http://localhost:8000/services/location/123

    ID is validated in urls config, no need to repeat here
    """

    location = LOCATION_SERVICE.get_location(id=id)
    if not location:
        raise Http404

    points = conversions.location_to_point(location)

    return json_response(points)

@csrf_exempt
def add_location(request): #, latitude, longitude, type, address=None, picture=None, description=None
    """
    TODO document
    TODO allow it to accept GeoJSON point as input too
    """
    # Validate request - must be POST
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Validate latitude - required, number only
    try:
        latitude = request.POST['latitude']
        latitude = float(latitude)
    except KeyError:
        return HttpResponseBadRequest('Missing latitude parameter')
    except ValueError:
        return HttpResponseBadRequest('Non-numeric latitude parameter')

    # Validate longitude - required, number only
    try:
        longitude = request.POST['longitude']
        longitude = float(longitude)
    except KeyError:
        return HttpResponseBadRequest('Missing longitude parameter')
    except ValueError:
        return HttpResponseBadRequest('Non-numeric longitude parameter')

    # Validate type - required, must be be a valid type
    try:
        type = request.POST['type']
        if not Location.VALID_TYPES.count(type):
            return HttpResponseBadRequest('Invalid type parameter. Valid options are: ' + str(Location.VALID_TYPES))
    except KeyError:
        return HttpResponseBadRequest('Missing type parameter. Valid options are ' + str(Location.VALID_TYPES))

    # Validate address - optional, must only have letters, numbers, periods, and dashes
    address = request.POST.get('address', None)
    if address and not VALID_ADDRESS_REGEX.match(address):
        return HttpResponseBadRequest(
            'Invalid address parameter. Can only contain letters, spaces, numbers, periods, and dashes')

    # Validate picture - optional, must be under a certain size limit
    # TODO figure out how to do this
    try:
        picture = request.FILES['picture']
    except KeyError:
        picture = None

    # Validate description - optional; limit to 200 characters; only letters, numbers, common punctuation, dashes
    try:
        description = request.POST['description']
        if description and len(description) > 200 and not VALID_DESCRIPTION_REGEX.match(description):
            return HttpResponseBadRequest(
                'Invalid description parameter. Can only contain periods, spaces, question marks, exclamations, letters, numbers, and dashes')
    except KeyError:
        description = None

    # Add the location
    try:
        location = LOCATION_SERVICE.add_location(latitude, longitude, type, address, picture, description)
    except Exception as e:
        return HttpResponseServerError('Was unable to add the new location due to an error: ' + e.message)

    # return the location that was just added
    return get_location_by_id(request, location.id)

@csrf_exempt
def update_location(request, id): # type=None, address=None, picture=None, description=None
    """
    TODO document
    TODO allow it to accept GeoJSON point as input too
    """
    # Validate request - must be POST
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Validate type - required, must be be a valid type
    try:
        type = request.POST['type']
        if not Location.VALID_TYPES.count(type):
            return HttpResponseBadRequest('Invalid type parameter. Valid options are: ' + str(Location.VALID_TYPES))
    except KeyError:
        type = None

    # Validate address - optional, must only have letters, numbers, periods, and dashes
    try:
        address = request.POST.get('address', None)
        if address and not VALID_ADDRESS_REGEX.match(address):
            return HttpResponseBadRequest(
                'Invalid address parameter. Can only contain letters, numbers, periods, spaces, and dashes')
    except KeyError:
        address = None

    # Validate picture - optional, must be under a certain size limit
    try:
        picture = request.FILES['picture']
    except KeyError:
        picture = None

    # Validate description - optional; limit to 200 characters; only letters, numbers, common punctuation, dashes
    try:
        description = request.POST['description']
        if description and len(description) > 200 and not VALID_DESCRIPTION_REGEX.match(description):
            return HttpResponseBadRequest(
                'Invalid description parameter. Can only contain spaces, periods, question marks, exclamations, letters, numbers, and dashes')
    except KeyError:
        description = None

    # Add the location
    try:
        location = LOCATION_SERVICE.update_location(id=id, type=type, address=address, picture=picture, description=description)
    except Exception as e:
        return HttpResponseServerError('Was unable to add the new location due to an error: ' + e.message)

    # return the location that was just updated
    if location:
        return get_location_by_id(request, location.id)
    else:
        return HttpResponseBadRequest("No update was made")

@csrf_exempt
def geocode(request, streetAddress):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    if not streetAddress:
        raise Http404

    # Try to get from cache first
    geocodeCaches = GeocodeCache.objects.filter(address=streetAddress.lower())
    if(geocodeCaches):
        points = conversions.geocode_caches_to_points(geocodeCaches)
        return json_response(points)

    # Retrieve from Geocoder
    # TODO parameterize some of this information in a config file
    params = {
        "apiKey": settings.TAMU_GEOCODING_API_KEY,
        "version": "4.01",
        "streetAddress": streetAddress,
        "city": "Philadelphia",
        "state": "PA",
        "allowTies": True,
        "format": "csv",
        "notStore": True,
        "includeHeader": False
    }

    r = requests.get("http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx", params=params)
    points = conversions.tamu_locations_to_points(r.text)

    # Save in cache
    for point in points:
        geocodeCache = GeocodeCache()
        geocodeCache.address = streetAddress.lower()
        geocodeCache.latitude = point["coordinates"][0];
        geocodeCache.longitude = point["coordinates"][1];
        geocodeCache.save()

    return json_response(points)