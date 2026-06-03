class dad :
    def __init__(self,eyes,height):
        self.eyes = eyes
        self.height = height
    def display(self):
        print("Your eye color is ",self.eyes)
        print("Your height is ",self.height)

class son(dad):
    def __init__(self,name,age,eyes, height):
        self.name = name
        self.age = age
         
        dad.__init__(self,eyes,height)