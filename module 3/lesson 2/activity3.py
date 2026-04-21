def fact(num):
    if num==0 or num==1:
        return 1
    else:
        return num*fact(num=1)

print("The factorial of 0:",fact(0))
print("The factorial of 1:",fact(1))
print("The factorial of 2:",fact(2))
print("The factorial of 60:",fact(60))