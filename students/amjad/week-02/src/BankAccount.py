class BankAccount:
    def __init__(self, money: int, num: int) -> None:
        self._is_valid_account_number(num)
        self._is_valid_money(money)
        self.__money = money
        self.num = num

    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        return cls(money=data["money"], num=data["num"])

    @staticmethod
    def _is_valid_account_number(num: int) -> None:
        if not isinstance(num, int) or num <= 0:
            raise ValueError("InvalidAccountNumberError")

    @staticmethod
    def _is_valid_money(money: int) -> None:
        if not isinstance(money, int) or money<0:
            raise ValueError("InvalidMoneyError")

    def deposit(self, add: int) -> None:
        if not isinstance(add, int) or add<=0:
            raise ValueError("InvalidDepositAmountError")

        self.__money += add

    def withdraw(self, subtract: int) -> None:
        if not isinstance(subtract, int) or subtract<=0:
            raise ValueError("InvalidWithdrawAmountError")

        if self.__money < subtract:
            raise ValueError("InsufficientFundsError")

        self.__money -= subtract

    def get_money(self) -> int:
        return self.__money


if __name__ == "__main__":
    dict1 = {"money":500, "num":12345}

    user = BankAccount.from_dict(dict1)
    user.deposit(100)
    print(user.get_money())

    try:
        dict2 = {"money": 500, "num": 'ss'}

        user2 = BankAccount.from_dict(dict2)
        user2.deposit(200)
        print(user2.get_money())

    except ValueError as error:
        print(error)