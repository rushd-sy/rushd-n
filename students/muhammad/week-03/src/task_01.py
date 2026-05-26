from dataclasses import dataclass

@dataclass
class BankAccount():
    full_name: str
    account_num: int
    __balance: float = 0.0

    @classmethod
    def from_dict(cls, dic: dict) -> "BankAccount":
        if 'account_num' not in dic:
            raise ValueError("Dictionary must contain 'account_num")
        if 'full_name' not in dic:
            raise ValueError("Dictionary must contain 'full_name")
        
        if 'initial_balance' in dic:
            return cls (dic['full_name'], dic['account_num'], dic['initial_balance']) 
        
        return cls (dic['full_name'], dic['account_num']) 
        
    @staticmethod
    def is_valid_account_number(num: int)-> bool:
        return isinstance(num, int) and int(num) >= 0

    def __init__(self, full_name: str, account_num: int, initial_balance: float = 0) -> None:
        if not self.is_valid_account_number(account_num):
            raise ValueError(f"Invalid account number format: {account_num}")
        self.full_name = full_name
        self.__balance = initial_balance
        self.account_num = account_num


    def deposit(self, deposit_amount: float) -> None:
        if deposit_amount <= 0:
            raise ValueError("Deposit amount should be positive, found nonpositive amount")
        self.__balance += deposit_amount

    def withdraw(self, withdraw_amount: float) -> None:
        if withdraw_amount > self.__balance:
            raise ValueError("""InsufficientFundsError""")        
        self.__balance -= withdraw_amount



    def get_balance(self) -> float:
        return self.__balance
