height = float(input("enter your height in CM: "))
weight = float(input("Enter your weight in kG: "))

bmi = weight / (height/100)**2
print("Your bmi is",bmi)

if bmi <= 18.4:
    print("You are underweight.")

elif bmi <= 24.9:
    print("You are healthy")

elif bmi <= 29.9:
    print("You are overweight")
elif bmi <= 34.9:
    print("You are obese")
else:
    print("You are severly obese.")