from geopy.geocoders import Nominatim
from Reader import *


def Euclidean(x, y):
    geolocator = Nominatim(user_agent="google maps")
    x_com = x + ', Boston, Massachusetts'
    y_com = y + ', Boston, Massachusetts'
    x_loc = geolocator.geocode(x_com)
    y_loc = geolocator.geocode(y_com)
    if x_loc is None:
        return x_com
    if y_loc is None:
        return y_com
    return None

From, To, Miles, G = readMyFile('St-Data-Original - Processed.csv')
text_file = open("sample.txt", "w")
for i in range(len(From)):
    val = Euclidean(From[i], To[i])
    if val!= None:
        text_file.write(val +"\n")
text_file.close()

'''
From, To, Miles, G = readMyFile('St-Data-Original - Processed.csv')

geolocator = Nominatim(user_agent="google maps")
avenue = geolocator.geocode("Cheslea St, Boston")
print(avenue.address)
print((avenue.latitude, avenue.longitude))
print(avenue.raw)

street = geolocator.geocode("Boylston Street, Boston")
print(street.address)
print((street.latitude, street.longitude))
print(street.raw)

street = geolocator.geocode("Fairfield Street, Boston")
print(street.address)
print((street.latitude, street.longitude))
print(street.raw)

street = geolocator.geocode("Dead End, Boston")
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
crossing = geolocator.geocode("Ditson Street at Draper Street, Boston")
print(crossing.address)
print((crossing.latitude, crossing.longitude))
print(crossing.raw)
'''