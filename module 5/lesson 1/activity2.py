class parrot:
    species = "bird"

    def __init__(self,name,age):
        self.name = name 
        self.age = age
blu = parrot("Blue",10)
woo = parrot("Woo",15)

print(f"The first parrot is {blu.name}.He is a {blu.species}. He is {blu.age}.")
print(f"The second parrot is {woo.name}. He is a {woo.species}. He is {woo.age}.")