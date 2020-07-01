import googlemaps

def getCoordinates(address):
	"""
	:param address:  address of the merchant in words
	:return: latitude and longitude coordinates for location using geocoding API
	"""
	gmaps = googlemaps.Client(key='AIzaSyAntxrxhQu11TxFD9wEe7JxxW1UZ0HQXRY')
	geocode_result = gmaps.geocode(address)
	return geocode_result


