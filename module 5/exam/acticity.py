class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def show(self):
        print("Balance:", self.__balance)

account = BankAccount(1000)
account.show()