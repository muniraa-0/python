s1 = (2,3,1)
s2 = {'b','c','a'}
s3 = list(zip(s1,s2))
print(s3)

stocks = ['relance','infoys','tcs']
prices = [2127,4566,3409]
new_dict = {
    stocks:prices for stocks,prices in zip(stocks,prices)
}
print(format(new_dict))