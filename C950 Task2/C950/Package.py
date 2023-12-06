class Package:
    def __init__(self, package_id: int, address: str, city: str, state: str,
                 zipcode: str, deadline_time, weight: float, status: str = "At the hub"):
        """
        Initializes the Package object with given attributes.

        :param package_id: Unique identifier for the package.
        :type package_id: int
        :param address: Delivery address for the package.
        :type address: str
        :param city: City of the delivery address.
        :type city: str
        :param state: State of the delivery address.
        :type state: str
        :param zipcode: Zipcode of the delivery address.
        :type zipcode: str
        :param deadline_time: Time by which the package should be delivered.
        :type deadline_time: datetime.datetime
        :param weight: Weight of the package.
        :type weight: float
        :param status: Current status of the package (default is "At the hub").
        :type status: str
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self) -> str:
        """
        Returns a string representation of the Package object.

        :return: A string detailing the package's attributes.
        :rtype: str
        """
        return (
            f"{self.package_id}, {self.address}, {self.city}, {self.state}, "
            f"{self.zipcode}, {self.deadline_time}, {self.weight}kg, "
            f"{self.delivery_time}, {self.status}"
        )

    def update_status(self, current_time):
        """
        Updates the status of the package based on its delivery and departure times in
        comparison to the provided current time.

        :param current_time: The current time to check against.
        :type current_time: datetime.datetime
        """
        if self.delivery_time and self.delivery_time <= current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En route"
        else:
            self.status = "At the hub"

