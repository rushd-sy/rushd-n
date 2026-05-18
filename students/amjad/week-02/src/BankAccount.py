class bank_account:
    def __init__(self, money = 0):
        self.money = money

    def deposit(self, add):
        self.money += add

    def withdraw(self, substract):
        if self.money < substract :
            raise ValueError("InsufficientFundsError")
        self.money -= substract

user = bank_account(500)
user.deposit(100)
print(user.money)
user.withdraw(500)
print(user.money)


user2 = bank_account()
user2.deposit(200)
print(user2.money)
user2.withdraw(500)
print(user2.money)
