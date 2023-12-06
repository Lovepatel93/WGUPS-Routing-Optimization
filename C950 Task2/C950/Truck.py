from typing import List, Optional
from datetime import timedelta


class Truck:
    def __init__(self,
                 capacity: int,
                 speed: float,
                 load: float = 0.0,
                 packages: Optional[List[int]] = None,
                 mileage: float = 0.0,
                 address: str = "",
                 depart_time: timedelta = timedelta()):
        """
        Initialize a Truck object.

        :param capacity: Maximum number of packages the truck can carry.
        :param speed: Average speed of the truck in miles per hour.
        :param load: Current weight the truck is carrying.
        :param packages: List of package IDs currently in the truck.
        :param mileage: Total distance the truck has covered.
        :param address: Current address of the truck.
        :param depart_time: Time the truck is scheduled to depart.
        """
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages if packages is not None else []  # Avoid mutable default arguments
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self) -> str:
        return (f"Capacity: {self.capacity}, Speed: {self.speed}, Load: {self.load}, "
                f"Packages: {self.packages}, Mileage: {self.mileage}, Address: {self.address}, "
                f"Departure Time: {self.depart_time}")
