class bank_account:
    def __init__(self, money = 0):
        self.money = money
        self.num = 0

    def from_dict(self, dict):
        self.money = dict["money"]
        self.is_valid_account_number(dict["num"])
        self.num = dict["num"]

    def is_valid_account_number(self, num):
        if not isinstance(num, int) or num <= 0:
            raise ValueError("InvalidAccountNumberError")

    def deposit(self, add):
        self.money += add

    def withdraw(self, substract):
        if self.money < substract :
            raise ValueError("InsufficientFundsError")
        self.money -= substract

dict1 = {"money": 500, "num": 12345}
user = bank_account()
user.from_dict(dict1)
user.deposit(100)
print(user.money)

dict2 = {"money": 500, "num": 'ss'}
user2 = bank_account()
user2.from_dict(dict2)
user2.deposit(200)
print(user2.money)