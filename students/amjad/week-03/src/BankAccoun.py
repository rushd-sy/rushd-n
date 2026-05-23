# the same in week 02 but with dataclass & pydantic
from dataclasses import dataclass

from pydantic import field_validator, BaseModel


@dataclass
class BankAccount:
    money: int
    num: int

    def __post_init__(self):
        self._is_valid_account_number(self.num)
        self._is_valid_money(self.money)
        self.__money = self.money
        self.num = self.num

    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        return cls(money=data["money"], num=data["num"])

    @staticmethod
    def _is_valid_account_number(num: int) -> None:
        if not isinstance(num, int) or num <= 0:
            raise ValueError("InvalidAccountNumberError")

    @staticmethod
    def _is_valid_money(money: int) -> None:
        if not isinstance(money, int) or money < 0:
            raise ValueError("InvalidMoneyError")

    def deposit(self, add: int) -> None:
        if not isinstance(add, int) or add <= 0:
            raise ValueError("InvalidDepositAmountError")

        self.__money += add

    def withdraw(self, subtract: int) -> None:
        if not isinstance(subtract, int) or subtract <= 0:
            raise ValueError("InvalidWithdrawAmountError")

        if self.__money < subtract:
            raise ValueError("InsufficientFundsError")

        self.__money -= subtract

    def get_money(self) -> int:
        return self.__money


class BankAccountPydantic(BaseModel):
    money: int
    num: int

    @field_validator("num")
    def validate_account_number(cls, num):
        if not isinstance(num, int) or num <= 0:
            raise ValueError("InvalidAccountNumberError")
        return num

    @field_validator("money")
    def validate_money(cls, money):
        if not isinstance(money, int) or money < 0:
            raise ValueError("InvalidMoneyError")
        return money
