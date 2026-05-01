import math


angle = float(input("Enter angle in degrees: "))


radian = math.radians(angle)


sin_value = math.sin(radian)
cos_value = math.cos(radian)
tan_value = math.tan(radian)


print("sin(", angle, ") =", sin_value)
print("cos(", angle, ") =", cos_value)
print("tan(", angle, ") =", tan_value)