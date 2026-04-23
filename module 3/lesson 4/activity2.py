try:
    num1,num2 = eval(input("Enter two numbers, separated by a comma:  "))
    result = num1/num2
    print("Result:",result)
except ZeroDivisionError:
    print("Division by zero is error !!")

except SyntaxError:
    print("Comma is missing. enter numbers separated by comma like this 1,2")
except:
    print("wrong input")
else:
    print("No error")
finally:
    print("This will execute no matter what")