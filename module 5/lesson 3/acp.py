class Vehicle:
    def __init__(self, capacity):
        self.capacity = capacity

    def fare(self):
        return self.capacity * 100  


class Bus(Vehicle):
    def fare(self):
        base_fare = super().fare()
        total_fare = base_fare + (base_fare * 0.10)  
        return total_fare


school_bus = Bus(50)

print("Total Bus Fare:", school_bus.fare())