class BMW:
    def speed(self):
        print("BMW runs at 250 km/h")

class Ferrari:
    def speed(self):
        print("Ferrari runs at 340 km/h")


for car in (BMW(), Ferrari()):
    car.speed()