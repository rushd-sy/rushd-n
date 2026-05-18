class BankAccount:
    def __init__(self, money : int = 0) -> None:
        self.__money = money
        self.num = 0

    def from_dict(self, dict: dict) -> None:
        self.__money = dict["money"]
        self.is_valid_account_number(dict["num"])
        self.num = dict["num"]

    def is_valid_account_number(self, num: int) -> None:
        if not isinstance(num, int) or num <= 0:
            raise ValueError("InvalidAccountNumberError")

    def deposit(self, add: int) -> None:
        self.__money += add

    def withdraw(self, substract: int) -> None:
        if self.__money < substract :
            raise ValueError("InsufficientFundsError")
        self.__money -= substract

    def get_money(self) -> int:
        return self.__money

if __name__ == "__main__":

    dict1 = {"money": 500, "num": 12345}
    user = BankAccount()
    user.from_dict(dict1)
    user.deposit(100)
    print(user.get_money())

    dict2 = {"money": 500, "num": 'ss'}
    user2 = BankAccount()
    user2.from_dict(dict2)
    user2.deposit(200)
    print(user2.get_money())