buying_price = float(input("Enter the buying price"))
selling_price = float(input("Enter the selling price"))

if selling_price > buying_price:
    amount = selling_price -  buying_price
    print("He has profit of",amount)

else:
    print("He has loss")