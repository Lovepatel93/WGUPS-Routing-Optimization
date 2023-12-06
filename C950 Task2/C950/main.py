# Author: Love Patel
# Student ID: 001344143
# Title: C950 - Data Structures and Algorithms II

import csv
import datetime
from datetime import timedelta
from typing import Optional

from Truck import Truck

from HashMap import HashMap
from Package import Package


def read_csv_file(file_path: str) -> list:
    """
    Reads the contents of a CSV file and returns a list of rows.

    :param file_path: Path to the CSV file to be read.
    :type file_path: str
    :return: A list containing rows of the CSV, each row is also a list.
    :rtype: list
    """
    with open(file_path, 'r') as file:
        csv_content = csv.reader(file)
        return list(csv_content)


# Read the distance information from the CSV file
distance_data = read_csv_file("DistanceFile.csv")

# Read the address information from the CSV file
address_data = read_csv_file("AddressFile.csv")

# Read the package information from the CSV file
package_data = read_csv_file("PackageFile.csv")


def load_package_data(filename, package_hash_table):
    """
    Loads package data from a CSV file and inserts them into a hash table.

    :param filename: The path to the CSV file containing the package data.
    :param package_hash_table: The hash table where package data will be stored.
    """

    with open(filename) as package_info:
        local_package_data = csv.reader(package_info)  # Rename to local_package_data or similar
        for row in local_package_data:
            package_id = int(row[0])  # Convert the package_id to an integer
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]

            # Parsing the deadline_time based on the format in the CSV file
            if row[5] == "EOD":
                deadline_time = datetime.datetime.strptime("11:59:59 PM", '%I:%M:%S %p')
            else:
                deadline_time = datetime.datetime.strptime(row[5], '%I:%M %p')

            # Assuming the weight in the CSV is always in format 'xx Kilos'. Extracting numerical value.
            weight = float(row[6].split()[0])

            # Default status is "At Hub"
            status = "At the Hub"

            # Create a package object
            package = Package(
                package_id=package_id,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                deadline_time=deadline_time,
                weight=weight,
                status=status
            )

            # Insert package data into the hash table
            package_hash_table.insert(package_id, package)


def distance_between_points(point_a: int, point_b: int) -> float:
    """
    Returns the distance between two points using distance data from a CSV.

    :param point_a: Index of the first point in the CSV distance matrix.
    :type point_a: int
    :param point_b: Index of the second point in the CSV distance matrix.
    :type point_b: int
    :return: Distance between the two points.
    :rtype: float
    """

    # Attempt to get the distance from the CSV matrix using the provided indices
    distance = distance_data[point_a][point_b]

    # If the distance is not found in the above cell (is empty), then get it from the transposed cell
    if not distance:
        distance = distance_data[point_b][point_a]

    # Convert the distance string to a float and return
    return float(distance)


def extract_address_number(address_str: str) -> int:
    """
    Extracts the address number from a given address string based on data from a CSV.

    :param address_str: The address string to search for in the CSV.
    :type address_str: str
    :return: The address number corresponding to the given address string.
    :rtype: int
    :raises: ValueError if the address string is not found in the CSV.
    """

    # Iterate through each row in the CSV address data
    for row in address_data:
        # Check if the provided address string exists within the current row's address field
        if address_str in row[2]:
            # Return the corresponding address number (assuming it's in the first column of the row)
            return int(row[0])

    # If no match found, raise a ValueError exception with a message
    raise ValueError(f"The address '{address_str}' was not found in the CSV.")


# Constants for truck attributes
TRUCK_MAX_CAPACITY = 16
TRUCK_SPEED = 18
HUB_ADDRESS = "4001 South 700 East"

# Truck 1: Loaded with specific packages and is scheduled to depart first at 8:00 am.
truck1_packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
truck1 = Truck(
    capacity=TRUCK_MAX_CAPACITY,
    speed=TRUCK_SPEED,
    packages=truck1_packages,
    address=HUB_ADDRESS,
    depart_time=timedelta(hours=8)
)

# Truck 2: Will depart at 10:20 am with its assigned packages.
truck2_packages = [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
truck2 = Truck(
    capacity=TRUCK_MAX_CAPACITY,
    speed=TRUCK_SPEED,
    packages=truck2_packages,
    address=HUB_ADDRESS,
    depart_time=timedelta(hours=10, minutes=20)
)

# Truck 3: Departs at 9:05 am with its package list, possibly those without early deadlines.
truck3_packages = [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33]
truck3 = Truck(
    capacity=TRUCK_MAX_CAPACITY,
    speed=TRUCK_SPEED,
    packages=truck3_packages,
    address=HUB_ADDRESS,
    depart_time=timedelta(hours=9, minutes=5)
)

# Initialize a hash table to store package data
package_table = HashMap()

# Load packages into hash table
load_package_data("PackageFile.csv", package_table)


def deliver_packages(truck):
    """
    Determine the delivery order for packages on a truck using the nearest neighbor algorithm.
    This function will:
    - Update the truck's package list in the order they should be delivered.
    - Calculate the mileage the truck drives.
    - Record the delivery time for each package.

    :param truck: An instance of the Truck class that is being used for delivery.
    :type truck: Truck
    """

    # Create a list of packages that are yet to be delivered using the truck's package list and the hash table.
    not_delivered = [package_table.lookup(packageID) for packageID in truck.packages]

    # Clear the truck's package list. We'll re-add packages in delivery order.
    truck.packages.clear()

    # Continue delivering packages as long as there are packages that have not been delivered.
    while not_delivered:
        # Initialize variables to keep track of the nearest package and its distance.
        nearest_distance = float('inf')
        nearest_package = None

        # For each undelivered package, determine its distance from the truck's current location.
        for package in not_delivered:
            current_distance = distance_between_points(extract_address_number(truck.address),
                                                       extract_address_number(package.address))

            # If this package is closer than previous packages, update our "nearest" tracking variables.
            if current_distance <= nearest_distance:
                nearest_distance = current_distance
                nearest_package = package

        # Add the nearest package's ID to the truck's package list.
        truck.packages.append(nearest_package.package_id)

        # Remove the delivered package from the not_delivered list.
        not_delivered.remove(nearest_package)

        # Update the truck's total mileage and address to reflect the delivery.
        truck.mileage += nearest_distance
        truck.address = nearest_package.address

        # Update the truck's current time by adding the time taken to travel to the nearest package.
        truck.time += datetime.timedelta(hours=nearest_distance / 18)

        # Set the delivery time of the package and the truck's departure time.
        nearest_package.delivery_time = truck.time
        nearest_package.departure_time = truck.depart_time


# Deliver packages for each truck in sequence.
# Truck1 starts its deliveries first.
deliver_packages(truck1)

# Then, Truck2 starts its deliveries.
deliver_packages(truck2)

# Truck3 starts its deliveries once the earliest of Truck1 or Truck2 has completed its deliveries.
truck3.depart_time = min(truck1.time, truck2.time)
deliver_packages(truck3)


class Main:
    @staticmethod
    def display_intro():
        """Display the introduction to the program."""
        # Print the welcome banner and introductory message
        print("\n" + "=" * 60)
        print(f"{'=' * 22} WGUPS PACKAGE TRACKER {'=' * 22}")
        print("=" * 60 + "\n")
        print("Welcome to the Western Governors University Parcel Service (WGUPS) package tracker!")
        print("With this system, you can check the status of packages at any given time.\n")
        # Display total mileage of all trucks
        print(f"Total mileage across all trucks today: {truck1.mileage + truck2.mileage + truck3.mileage} miles\n")
        print("=" * 60 + "\n")

    @staticmethod
    def get_user_time() -> Optional[datetime.timedelta]:
        """Get user input for time and return as a timedelta."""
        while True:
            # Prompt the user to input a time or type 'back'
            user_time = input(
                "Enter a time (HH:MM:SS) to check the package status or 'back' to return to the main menu: ")

            # If the user types 'back', exit the loop
            if user_time.lower() == 'back':
                return None
            try:
                # Split input into hours, minutes, and seconds
                h, m, s = user_time.split(":")
                return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            except ValueError:
                # If there's an error in the format of the input, show an error message
                print("Invalid format. Please enter time as HH:MM:SS.")

    @staticmethod
    def display_package_status(time: datetime.timedelta):
        """Display the package status based on user preference (all or solo)."""
        while True:
            # Ask if the user wants to update the current time
            change_time = input("Would you like to change the time before checking package status? (yes/no): ").lower()
            if change_time == 'yes':
                new_time = Main.get_user_time()
                if new_time is not None:
                    time = new_time
                print(f"Time has been updated to: {time}")

            # Display package status options
            print("\nChoose an option to view package status:")
            print("1. Specific package by ID")
            print("2. All packages")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            # Handle the user's choice
            if choice == '1':
                # Prompt for a specific package ID
                package_id = input("Enter the package ID you want to view (1-40): ")
                try:
                    package_id_num = int(package_id)
                    if package_id_num < 1 or package_id_num > 40:
                        print("Invalid package ID. Please enter a number between 1 and 40.")
                        continue
                    package = package_table.lookup(package_id_num)
                    package.update_status(time)
                    print(str(package))
                except ValueError:
                    print("Invalid entry. Please enter a numeric ID between 1 and 40.")
            elif choice == '2':
                # Display the status of all packages
                for packageID in range(1, 41):
                    package = package_table.lookup(packageID)
                    package.update_status(time)
                    print(str(package))
            elif choice == '3':
                # Exit the program
                exit()
            else:
                # Handle invalid choices
                print("Invalid choice. Please enter a valid option (1/2/3).")

    @classmethod
    def run(cls):
        """Main function to run the program."""
        cls.display_intro()

        # Initialize current time to 00:00:00
        current_time = datetime.timedelta(hours=0, minutes=0, seconds=0)

        while True:
            # Display the main menu options
            print("\nMain Menu:")
            print("1. Update/check time")
            print("2. Check package status")
            print("3. Exit")

            main_choice = input("Enter your choice (1/2/3): ")

            if main_choice == "1":
                # Update or check the current time
                new_time = cls.get_user_time()
                if new_time:  # If time was provided and not 'back'
                    current_time = new_time
                print(f"Current Time: {current_time}")

            elif main_choice == "2":
                # Check package status
                if not current_time:
                    current_time = cls.get_user_time()
                while current_time:
                    cls.display_package_status(current_time)
                    # Provide an option to continue checking or return to the main menu
                    print("\nChoose an option to continue:")
                    print("1. Check another package")
                    print("2. Return to main menu")
                    sub_choice = input("Enter your choice (1/2): ")
                    if sub_choice == "2":
                        break

            elif main_choice == "3":
                # Exit the program
                print("Exiting. Have a good day!")
                exit()

            else:
                # Handle invalid main menu choices
                print("Invalid choice. Please select a valid option from the menu.")


# To run the program
Main.run()







