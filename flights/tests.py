from django.test import Client, TestCase
from .models import Flight, Passenger, Airport

# Create your tests here.

class FlightModelTests(TestCase):
    def setUp(self):
        a1 = Airport.objects.create(code="JFK", city="New York")
        a2 = Airport.objects.create(code="LAX", city="Los Angeles")
        
        Flight.objects.create(origin=a1, destination=a2, duration=300)
        Flight.objects.create(origin=a2, destination=a1, duration=320)
        Flight.objects.create(origin=a1, destination=a1, duration=100)

        p1 = Passenger.objects.create(first_name="John", last_name="Doe")
        p2 = Passenger.objects.create(first_name="Jane", last_name="Smith")

    def test_departure_count(self):
        jfk = Airport.objects.get(code="JFK")
        self.assertEqual(jfk.departures.count(), 2)
    
    def test_arrival_count(self):
        jfk = Airport.objects.get(code="JFK")
        self.assertEqual(jfk.arrivals.count(), 2)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="JFK")
        a2 = Airport.objects.get(code="LAX")
        flight = Flight.objects.get(origin=a1, destination=a2, duration=300)
        self.assertTrue(flight.is_valid_flight())

    def test_invalid_flight_same_origin_destination(self):
        a1 = Airport.objects.get(code="JFK")
        flight = Flight.objects.get(origin=a1, destination=a1, duration=100)
        self.assertFalse(flight.is_valid_flight())

    def test_invalid_flight_negative_duration(self):
        a1 = Airport.objects.get(code="JFK")
        a2 = Airport.objects.get(code="LAX")
        flight = Flight.objects.create(origin=a1, destination=a2, duration=-50)
        self.assertFalse(flight.is_valid_flight())

    def test_index(self):
        c= Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_flight_page(self):
        c = Client()
        flight = Flight.objects.first()
        response = c.get(f"/{flight.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flight"].id, flight.id)

    def test_invalid_flight_page(self):
        c = Client()
        max_id = Flight.objects.all().order_by("id").last().id
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        c = Client()
        flight = Flight.objects.first()
        p1 = Passenger.objects.get(first_name="John", last_name="Doe")
        p2 = Passenger.objects.get(first_name="Jane", last_name="Smith")
        
        flight.passengers.add(p1)

        response = c.get(f"/{flight.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(p1, response.context["passengers"])
        self.assertIn(p2, response.context["non_passengers"])

    

    