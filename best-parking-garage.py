from random import randint
import time


class ParkingGarage():

    '''
        ParkingGarage class to be used with open_garage function
        Takes one argument during instantiation, namely the number of parking spaces in the lot
        enter_garage method invoked when a car enters the garage
        exit_garage method invoked and asks for payment when a car leaves the garage
        empty_till method to collect people's payment
        view_status method shows how many cars are in the lot, how many open spaces, current ticket numbers
    '''

    def __init__(self, parking_spaces):
        self.parking_spaces = parking_spaces
        # should be called cars_in_garage:
        self.current_space = 0
        # no identical ticket numbers:
        self.current_tickets = set()
        # stores people's payment - they can pay with pocket lint, or whatever, has to be some "amount":
        self.till = ""
        # included "paid" key because it was in the assignment, but probably unnecessary:
        self.lot_status = dict([(parking_space, {"paid": True, "time entered": 0})
                                for parking_space in range(parking_spaces)])

    def enter_garage(self):
        if self.current_space != self.parking_spaces:
            ticket_number = randint(1001, 9999)
            # ensures there are no duplicate ticket numbers active:
            while ticket_number in self.current_tickets:
                # good for lots with up to 8998 parking spaces:
                ticket_number = randint(1001, 9999)
            self.current_tickets.add(ticket_number)
            print(f"\nPlease take your ticket: {ticket_number}")
            # sets dict key to ticket number, using current_space counter to avoid iterating each time:
            self.lot_status[ticket_number] = self.lot_status.pop(
                self.current_space)
            # time stamp:
            self.lot_status[ticket_number]["time entered"] = time.time()
            self.lot_status[ticket_number]["paid"] = False
            self.current_space += 1
        else:
            print("\nParking Full")

    def exit_garage(self, ticket_number):
        if ticket_number in self.current_tickets:
            stay_duration = time.time() - \
                self.lot_status[ticket_number]["time entered"]
            payment = input(
                f"\nYou were parked for {stay_duration} seconds. To pay, enter any amount, or anything you have in your pockets will be fine. Really anything will do: ")
            # makes them pay to leave:
            while payment == "":
                payment = input(
                    "\nYou have to pay. Anything will do, just enter something:")
            print("\nThank you! Have a nice day!")
            self.till += payment
            self.lot_status[ticket_number]["paid"] = True
            self.lot_status[ticket_number]["time entered"] = 0
            self.current_tickets.remove(ticket_number)
            self.current_space -= 1
            # resets dict key:
            self.lot_status[self.current_space] = self.lot_status.pop(
                ticket_number)
        else:
            print("\nTicket Not Found")

    def empty_till(self):
        print(f"\nHere is what was in the till: {self.till}")
        self.till = ""
        print("\nThe till is now empty.")

    def view_status(self):
        print(f"\nCars in garage: {self.current_space}")
        print(
            f"\nAvailable parking spaces: {self.parking_spaces - self.current_space}")
        print(f"\nCurrent ticket numbers: {self.current_tickets}")


def open_garage(parking_garage):
    '''
        open_garage function to be used with ParkingGarage class
        there are a few input options that are not specifically prompted for
        "empty till", "view status", and "close garage"
    '''
    # I don't know if this is any better than looping while true, but it looks better:
    garage_open = True
    while garage_open:
        entry_kiosk = input(
            "\nTo enter the garage, press 'Enter'. To exit the garage, please enter ticket number: ").lower()
        try:
            ticket_number = int(entry_kiosk)
        except ValueError:
            if entry_kiosk == "":
                parking_garage.enter_garage()
            elif entry_kiosk == "empty till":
                parking_garage.empty_till()
            elif entry_kiosk == "view status":
                parking_garage.view_status()
            elif entry_kiosk == "close garage":
                parking_garage.empty_till()
                parking_garage.view_status()
                garage_open = False
            else:
                print("Invalid Entry")
        else:
            if 1001 <= ticket_number <= 9999:
                parking_garage.exit_garage(ticket_number)
            else:
                print("Ticket Number Must Be 4 Digits")


airport_parking = ParkingGarage(6)
open_garage(airport_parking)
