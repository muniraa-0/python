num = [1,2,3,4]
num2 = [5,6,7,8]

result = map(lambda x,y: x'y, num1,num2)
print("Addition:" ,list(result))

nums = [1,2,3,4,5,6]

def square(n):
    return n*n

square = list(map(square,nums))
print("Mapped Values",square)