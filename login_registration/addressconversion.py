from datetime import datetime
import googlemaps
import json
def getCoordinates(address):
	
	gmaps = googlemaps.Client(key='AIzaSyAntxrxhQu11TxFD9wEe7JxxW1UZ0HQXRY')
	geocode_result = gmaps.geocode(address)
	
	return geocode_result
	#[0]['geometry']['location']


