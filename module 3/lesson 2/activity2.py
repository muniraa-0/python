def by_three(number):
    if number%3==0:
      return cube(number)
    else:
        return False

def cube(number):
    return number*number*number

number = int(input("Enter the number: "))
print(by_three(number))  