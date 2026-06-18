class square:
    def __init__(self,side):
        self.side = side
    
    def area(self):
        print("Area of square:",self.side**2)

class rectangle:
    def __init__(self,side1,side2):
        self.side1 = side1
        self.side2 = side2
    def area(self):
        print("Area of rectangle:",self.side1*self.side2)
class circle:
    def __init__(self,radius):
        self.radius = radius

    def area(self):
        print("Area of circ;e:",3.14*self.radius**2)

osquare = square(5)
orect = rectangle(2,4)
ocircle = circle(2)

for x in (osquare,orect,ocircle):
    x.area()