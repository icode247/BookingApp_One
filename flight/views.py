from django.shortcuts import render
from amadeus import Client, ResponseError, Location
from django.http import JsonResponse

amadeus = Client(
    client_id='CoArtPgeKZ5667oYQFCkFCBsv5PeV43Q',
    client_secret='PbkxxwJuP5xL5aqX'
)

def select_destination(req, param):
     if req.method == "GET":
        try:
            print(param)
            response = amadeus.reference_data.locations.get(
                keyword=param, subType=Location.ANY)
            context = {
                "data": response.data
            }
            return JsonResponse(context)
        except ResponseError as error:
            print(error)
     else:
        return JsonResponse({"error": "Invalid request method"})

def search_offers(req):
    if req.method == "GET":
        try:
            origin_code = req.GET["originCode"]
            destination_code = req.GET["destinationCode"]
            departure_date = req.GET["departureDate"]
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code, destinationLocationCode=destination_code, departureDate=departure_date, adults=1)
            context = {
                "data": response.data
            }
            return JsonResponse(context)
        except ResponseError as error:
           print(error)
    else:
       return JsonResponse({"error": "Invalid request method"})


def price_offer(req):
   if req.method == "POST":
        try:
            flight = req.POST['flight']
            response = amadeus.shopping.flight_offers.pricing.post(flight)
            print(response.data)
            return JsonResponse(response.data)
        except ResponseError as error:
            print(error)
   else:
       return JsonResponse({"error": "Invalid request method"})

def book_flight(req):
    if req.method == "POST":
        try:
            flight = req.POST['flight']
            traveler = req.POST['traveler']
            booking = amadeus.booking.flight_orders.post(flight, traveler)
            return JsonResponse(booking)
        except ResponseError as error:
            print(error)
    else:
       return JsonResponse({"error": "Invalid request method"})
