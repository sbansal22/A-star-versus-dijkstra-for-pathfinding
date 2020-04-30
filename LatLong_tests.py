import googlemaps
from datetime import datetime
from opencage.geocoder import OpenCageGeocoder

# Google's Direction API
gmaps = googlemaps.Client(key='Add Your Key here')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# OpenCage's Geocoder API

geocoder = OpenCageGeocode('YOUR-API-KEY')

reverse = geocoder.reverse_geocode(14.66667, 75.83333)

forward = geocoder.geocode("Krishnamurti Puram, Mysore, India")