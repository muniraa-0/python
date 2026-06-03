class person:
    def __init__(self,name,idnumber):
        self.namne = name
        self.idnumber = idnumber
    def display(self):
        print(f"Your name is",self.name)
        print(f"Your id number is",self.idnumber)
class employee(person):
    def __init__(self, name, idnumber,salary,post):
        self.salary = salary
        self.post = post
        super().__init__(name,idnumber)
ob = employee("Rahul",1011,100000,"manager")
ob.display()
print(f"My monthly salary is BDT {ob.salary}. i work as a {ob.post}.")
