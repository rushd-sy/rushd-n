from pydantic import BaseModel, PrivateAttr, field_validator

class BankAccount(BaseModel):
    full_name: str
    account_num: int
    __balance: float = PrivateAttr(default=0.0)

    @classmethod
    def from_dict(cls, dic: dict) -> "BankAccount":
        if 'account_num' not in dic:
            raise ValueError("Dictionary must contain 'account_num")
        if 'full_name' not in dic:
            raise ValueError("Dictionary must contain 'full_name")
        
        if 'initial_balance' in dic:
            return cls (full_name=dic['full_name'], account_num=dic['account_num'], initial_balance=dic['initial_balance']) 
        
        return cls (full_name=dic['full_name'], account_num=dic['account_num']) 

    @field_validator('account_num')
    def is_valid_account_number(num)-> bool:
        if not (isinstance(num, int) and int(num) >= 0):
            raise ValueError(f"Invalid account number format: {num}")
        return True

    def __init__(self, **data) -> None:
        super().__init__(**data)
        init_balance = data.pop('initial_balance', 0)
        self.__balance = init_balance
        print(f"Account was created with ${init_balance} initial balance.")



    def deposit(self, deposit_amount: float) -> None:
        if deposit_amount <= 0:
            raise ValueError("Deposit amount should be positive, found nonpositive amount")

        self.__balance += deposit_amount
        print(f"""Deposit completed successfully..
Old balance: ${self.__balance - deposit_amount}
New balance: ${self.__balance}
""")


    def withdraw(self, withdraw_amount: float) -> None:
        if withdraw_amount > self.__balance:
            raise ValueError("""InsufficientFundsError""")
        
        self.__balance -= withdraw_amount
        print(f"""Withdraw completed successfully..
Old balance: ${self.__balance + withdraw_amount}
New balance: ${self.__balance}
""")


    def get_balance(self) -> float:
        return self.__balance
