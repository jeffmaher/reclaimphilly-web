# REST API

This document outlines the web services supported by Reclaim Cities.

Most of the API returns [GeoJSON](http://www.geojson.org/) `Point` objects, along with some of custom properties inside the `properties` field (such as `address` or `description`).

## Add Location

This adds a location to the system along with relevant details.

It returns the added GeoJSON `Point` if successful. If it fails, it sends an HTTP Bad Request status code (400).

### Address

`/services/location`

### Arguments

#### Query Arguments

- `address`: Street address of the location. Do not include the city, state, zip, etc. Just street address.
- `description`: A description of the location
- `latitude`: The latitude of the location
- `longitude`: The longitude of the location
- `lot_type`: The type of location. The following values are valid:
	- `LOT`: Lot
	- `RES`: Residential
	- `NRS`: Non-residential

#### POST Body Arguments

- `picture1` (optional): An image file of the location
- `picture2` (optional): An image file of the location
- `picture3` (optional): An image file of the location

### POST Request Example

`/services/location?address=1500%20s%2017th%20st&description=I%20added%20this %20location&latitude=39.9766090206&longitude=-75.163548700326&lot_type=RES`

or prior to encoding:

`/services/location?address=1500 s 17th st&description=I added this location&latitude=39.9766090206&longitude=-75.163548700326&lot_type=RES`

### POST Response Example

	{
	  "type": "Point",
	  "properties": {
	    "description": "I added this location",
	    "lot_type": "res",
	    "id": 4,
	    "address": "1500 s 17th st"
	  },
	  "coordinates": [
	    39.9766090206,
	    -75.163548700326
	  ]
	}


## Geocode

Converts an address to GeoJSON `Point` with latitude and longitude coordinates.

### Address

`/services/geocode/{street address}`

### Arguments

- `street address`: A street address within the configured city bounds. Must match regex [\w\s,.-]* .

### GET Request Example

Assuming the configured city is Philadelphia, PA, USA; and the address is `1600 S 17th St, Philadelphia, PA, USA`, the call would look like this:

`/services/geocode/1600%20S%2017th%20St`

or before encoding:

`/services/geocode/1600 S 17th St`

### GET Response Example

	[
	  {
	    "type": "Point",
	    "properties": {
	      "address": "1600 s 17th st"
	    },
	    "coordinates": [
	      39.931112187835,
	      -75.173280578901
	    ]
	  }
	]

The `address` property will not be populated by the default geocoder, but if the location is already in the system, there will be an `address` value.

### Notes

The geocoder is currently built under the assumption that the address is a USA city. The default geocoder is based on Texas A&M's system that derives from USA Census data.

## Location Details

Gets the GeoJSON `Point` for a location added to the system by ID. If the location does not exist in the system, a 404 HTTP code is returned.

### Address

`/services/location/{id}`

### Arguments

- `id`: The location ID. This can be found in the `properties` field of `Point` objects (such as from the Location Search command)

### GET Request Example

Getting details for location #1:

`/services/location/1`

### GET Response Example

	{
	  "type": "Point",
	  "properties": {
	    "pictures": [
	        "\/media\/images\/locations\/img1.jpg",
            "\/media\/images\/locations\/img2.jpg",
            "\/media\/images\/locations\/img3.jpg"
        ],
	    "description": "Test Non-residential",
	    "type": "nrs",
	    "id": 1,
	    "address": "1600 s 17th st"
	  },
	  "coordinates": [
	    39.931112187835,
	    -75.173280578901
	  ]
	}

## Location Search

Gets all locations in the system within a defined distance of a latitude and longitude coordinate.

### Address

/locations?latitude={latitude}&longitude={latitude}&radius={radius}

### Arguments

- `latitude`: The latitude at the center of your search radius
- `longitude`: The longitude at the center of your search radius
- `radius`: The distance in miles from the latitude and longitude coordinates in which a location must be to be returned

### GET Request Example

Searching for locations within a 1/2 mile radius of 1600 S 17th St would look like:

`http://localhost:8000/services/locations?latitude=39.9309936401893&longitude=-75.1730079892385&radius=0.5`

### GET Response Example

Assuming there are three locations near 1600 S 17th St, the following would be returned:

	[
	  {
	    "type": "Point",
	    "properties": {
	      "pictures": [
	        "\/media\/images\/locations\/img1.jpg",
            "\/media\/images\/locations\/img2.jpg"
	      ],
	      "description": "Test Non-residential",
	      "lot_type": "nrs",
	      "id": 1,
	      "address": "1600 s 17th st"
	    },
	    "coordinates": [
	      39.931112187835,
	      -75.173280578901
	    ]
	  },
	  {
	    "type": "Point",
	    "properties": {
	      "pictures": ["\/media\/images\/locations\/img3.jpg"],
	      "description": "Test lot",
	      "lot_type": "lot",
	      "id": 2,
	      "address": "1700 S 17th St"
	    },
	    "coordinates": [
	      39.929895293265,
	      -75.17355315703
	    ]
	  },
	  {
	    "type": "Point",
	    "properties": {
	      "pictures": ["\/media\/images\/locations\/img4.jpg"],
	      "description": "Test residential",
	      "lot_type": "res",
	      "id": 3,
	      "address": "1600 S 16th St"
	    },
	    "coordinates": [
	      39.930837986623,
	      -75.171834403502
	    ]
	  }
	]

## Location Update

The command allows the properties to be updated on an existing location within the system.

It returns the updated GeoJSON `Point`.

### Address

`/services/location/{id}/update`

### Arguments

#### URL Arguments

- `id`: The location ID. This can be found in the `properties` field of `Point` objects (such as from the Location Search command)

#### Query Arguments:

All query arguments are optional. The properties of the location will not be updated or removed if not specified, but will retain their existing values.

- `address`: The updated address for the location
- `description`: The updated description for the location
- `lot_type`: The updated type for the location. Can be one of the following fields:
	- `LOT`: Lot
	- `RES`: Residential
	- `NRS`: Non-residential

#### POST Body Arguments

- `picture1` (optional): An image file of the location
- `picture2` (optional): An image file of the location
- `picture3` (optional): An image file of the location

### POST Request Example

`POST`ing a description update to location #1:

`/services/location/1/update?description=I%20updated%20this%20location's%20details!`

or prior to encoding:

`/services/location/1/update?description=I updated this location's details!`

### POST Response Example

	{
	  "type": "Point",
	  "properties": {
	    "pictures": [
	        "\/media\/images\/locations\/img1.jpg",
            "\/media\/images\/locations\/img2.jpg"
	    ],
	    "description": "I updated this location's details!",
	    "lot_type": "nrs",
	    "id": 1,
	    "address": "1600 s 17th st"
	  },
	  "coordinates": [
	    39.931112187835,
	    -75.173280578901
	  ]
	}

