amount = int(input("Enter the amount: "))
tk_100 = amount//100
tk_50 = (amount%100)//50
tk_10 = ((amount%100)%50)//10
print("Notes of 100 taka: ",tk_100)
print("Notes of 50 taka: ",tk_50)
print("Notes of 10 taka: ",tk_10)