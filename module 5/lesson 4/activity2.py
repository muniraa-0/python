class computer:
    def __init__(self):
        self._maxprice = 900

    def sell(self):
        print(self.__maxprice)

    def setmaxprice(self,price):
        self.__maxprice = price

c = computer()
c.sell()
c.__maxprice = 1200
c.sell()
c.setmaxprice()
c.sell()