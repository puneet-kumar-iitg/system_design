'''
Entities
ParkingLot
    ParkingFloor
        ParkingSpot
Vehicle
Ticket
Pricing -> PricingStrategy
Parking -> ParkingStrategy
'''

import time
from abc import ABC, abstractmethod
from enum import Enum

class VehicleType(Enum):
    BIKE = "bike"
    CAR = "car"
    TRUCK = "truck"

class ParkingSpotType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3


class ParkingLot:

    def __init__(self, pricing_strategy, parking_strategy):
        self.floors = []
        self.tickets = {}
        self.pricing_strategy = pricing_strategy
        self.parking_strategy = parking_strategy

    def add_floor(self, floor):
        self.floors.append(floor)

    def park_vehicle(self, vehicle, ticket_id: str):
        spot = None
        # find spot in each floor if not found raise ValueError()
        spot = self.parking_strategy.find_spot(self.floors, vehicle)

        if not spot:
            raise ValueError("Parking is full.")

        # park vehicle
        spot.park(vehicle)

        # create ticket
        ticket = Ticket(
            ticket_id,
            vehicle,
            spot
        )
        self.tickets[ticket_id] = ticket
        return ticket

    def exit_vehicle(self, ticket_id):
        # find ticket data
        ticket = self.tickets.get(ticket_id)

        exit_time = int(time.time())

        amount = self.pricing_strategy.calculate_amount(ticket, exit_time)

        ticket.close(amount, exit_time)

        ticket.spot.remove()

        return amount


class ParkingFloor:

    def __init__(self, floor_id: int, name: str):
        self.floor_id = floor_id
        self.name = name
        self.spots = []

    def add_spot(self, spot):
        self.spots.append(spot)

    def find_parking_spot(self, vehicle):
        for spot in self.spots:
            if spot.can_park(vehicle):
                return spot
        return None


class ParkingSpot:

    SPOT_COMPATIBILITY = {
        ParkingSpotType.BIKE: (VehicleType.BIKE,),
        ParkingSpotType.CAR: (VehicleType.BIKE, VehicleType.CAR),
        ParkingSpotType.TRUCK: (VehicleType.BIKE, VehicleType.CAR, VehicleType.TRUCK)
    }

    def __init__(self, spot_id: int, spot_type: int):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.vehicle = None

    def is_available(self):
        return self.vehicle is None

    def can_park(self, vehicle):
        if not self.is_available():
            return False
        return vehicle.vehicle_type in self.SPOT_COMPATIBILITY.get(self.spot_type)
        


    def park(self, vehicle):
        self.vehicle = vehicle

    def remove(self):
        vehicle = self.vehicle
        self.vehicle = None
        return vehicle

class Vehicle:

    def __init__(self, number: str, vehicle_type: VehicleType):
        self.number = number
        self.vehicle_type = vehicle_type


class Ticket:

    def __init__(self, ticket_id: int, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = int(time.time())
        self.exit_time = None
        self.amount = None


    def close(self, amount: float, exit_time: int):
        self.amount = amount
        self.exit_time = exit_time

class PriningStrategy(ABC):

    @abstractmethod
    def calculate_amount(self):
        pass


class HourlyPriningStrategy(PriningStrategy):

    PARKING_RATE = {
        VehicleType.BIKE: 20,
        VehicleType.CAR: 50,
        VehicleType.TRUCK: 100
    }

    def calculate_amount(self, ticket, exit_time):
        duration = int(exit_time - ticket.entry_time)

        hours = duration//3600

        amount = max(1, hours * self.PARKING_RATE.get(ticket.vehicle.vehicle_type))

        return amount

    
class ParkingStrategy(ABC):

    @abstractmethod
    def find_spot(self):
        pass


class FirstAvailableParkingStrategy(ParkingStrategy):

    def find_spot(self, floors, vehicle):
        for floor in floors:
            spot = floor.find_parking_spot(vehicle)
            if spot:
                return spot
        return None
    
if __name__ == "__main__":
    pricing_strategy = HourlyPriningStrategy()
    parking_strategy = FirstAvailableParkingStrategy()
    parking_lot = ParkingLot(pricing_strategy, parking_strategy)

    floor_1 = ParkingFloor(101, "First Floor")
    floor_1.add_spot(
        ParkingSpot(1000, ParkingSpotType.BIKE)
    )
    floor_1.add_spot(
        ParkingSpot(1001, ParkingSpotType.CAR)
    )
    floor_1.add_spot(
        ParkingSpot(1002, ParkingSpotType.BIKE)
    )
    floor_1.add_spot(
        ParkingSpot(1002, ParkingSpotType.TRUCK)
    )

    parking_lot.add_floor(floor_1)

    car_1 = Vehicle("HR981234", VehicleType.CAR)
    bike_1 = Vehicle("HR981235", VehicleType.CAR)
    car_2 = Vehicle("HR981236", VehicleType.CAR)
    bike_2 = Vehicle("HR981237", VehicleType.BIKE)

    vehicle_list = [car_1, bike_1, car_2, bike_2]

    for it,veh in enumerate(vehicle_list):
        ticket = parking_lot.park_vehicle(veh, 10000+it)


        print(f"Entry : {ticket.entry_time}")

        amount = parking_lot.exit_vehicle(ticket.ticket_id)

        print(f"Amount : {amount} for Ticket : {ticket.ticket_id} Exit Time : {ticket.exit_time}")



