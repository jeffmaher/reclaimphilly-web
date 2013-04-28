# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from forms import AddLocation
from reclaimcities.libs.services import LocationService
from reclaimcities.apps.web.models import Location

LOCATION_SERVICE = LocationService()


def index(request):
    return map(request)

def map(request):
    return render_to_response("map.html")

def blog(request):
    return render_to_response("blog.html")

def help(request):
    return render_to_response("help.html")

def resources(request):
    return render_to_response("resources.html")

def about(request):
    return render_to_response("about.html")


def add_location(request):
    if(request.method == "POST"):
        form = AddLocation(request.POST, request.FILES)

        if(form.is_valid()):
            location = form.save()
            return HttpResponseRedirect("/location/" + str(location.id))

        return render(request, "add.html", {"form":form})
    else:
        form = AddLocation()

        return render(request, "add.html",
            dict({"form":form}.items() + request.GET.items()) # Adds on the address, latitude, and longitude
        )

def update_location(request, id=None):

    locations = Location.objects.filter(id=id)
    if len(locations) != 1:
        return HttpResponseBadRequest("Location with id " + id + " does not exist. Cannot update.")
    location = locations[0]

    if request.method == "POST":
        updateData = location.__dict__
        updateFiles = {"picture":location.picture}

        # Set fields the form/request doesn't have set
        if 'description' in request.POST:
            updateData['description'] = request.POST['description']

        if 'type' in request.POST:
            updateData['type'] = request.POST['type']

        if 'picture' in request.FILES:
            updateFiles['picture'] = request.FILES['picture']

        if 'picture-clear' in request.POST:
            updateFiles['picture'] = None
            updateData['picture-clear'] = request.POST['picture-clear']

        form = AddLocation(data=updateData, files=updateFiles, instance=location)
        if form.is_valid():
            location = form.save()
            return HttpResponseRedirect("/location/" + str(location.id))

        return render(request, "update.html", {"form":form, "id":id})
    else:
        form = AddLocation(instance=location)

        return render(request, "update.html",{"form":form, "id":id}) # Adds on the address, latitude, and longitude

def view_location(request, id):
    if(request.method != "GET"):
        return HttpResponseForbidden("Only GET requests supported")

    # Get the Location to display
    location = LOCATION_SERVICE.get_location(id=id)
    if not location:
        return HttpResponseNotFound("Could not find the location with ID " + id)

    return render_to_response("view.html", {"location":location})
