from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="google maps")
avenue = geolocator.geocode("Fisher Avenue, Boston")
print(avenue.address)
print((avenue.latitude, avenue.longitude))
print(avenue.raw)

street = geolocator.geocode("Boylston Street, Boston")
print(street.address)
print((street.latitude, street.longitude))
print(street.raw)

Euclidean_Distance_1 = ((street.latitude-avenue.latitude)**2 + (street.longitude-avenue.longitude)**2)**0.5
print('\nEuclidean Distance between Fisher Avenue and Boylstron Street is: ' + str(Euclidean_Distance_1) +'\n')

way = geolocator.geocode("David G Mugar Way, Boston")
print(way.address)
print((way.latitude, way.longitude))
print(way.raw)

Euclidean_Distance_2 = ((street.latitude-way.latitude)**2 + (street.longitude-way.longitude)**2)**0.5
print('\nEuclidean Distance between David G Mugar Way and Boylstron Street is: ' + str(Euclidean_Distance_2) +'\n')

# There is a crossing of Ditson Street and Draper Street
# crossing = geolocator.geocode("Ditson Street and Draper Street, Boston")
# print(crossing.address)
# print((crossing.latitude, crossing.longitude))
# print(crossing.raw)