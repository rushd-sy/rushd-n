class BankAccount():

    @classmethod
    def from_dict(cls, dic: dict):
        if 'account_num' not in dic:
            raise ValueError("Dictionary must contain 'account_num")
        if 'full_name' not in dic:
            raise ValueError("Dictionary must contain 'full_name")
        
        if 'initial_balance' in dic:
            return cls (dic['full_name'], dic['account_num'], dic['initial_balance']) 
        
        return cls (dic['full_name'], dic['account_num']) 
        
    @staticmethod
    def is_valid_account_number(num)-> bool:
            return isinstance(num, int)

    def __init__(self, full_name: str, account_num: int, initial_balance: float = 0) -> None:
        if not self.is_valid_account_number(account_num):
            raise ValueError(f"Invalid account number format: {account_num}")
        self.full_name = full_name
        self.__balance = initial_balance
        self.account_num = account_num
        print(f"Account was created with ${initial_balance} initial balance.")



    def deposit(self, deposit_amount: float) -> None:
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




# bitar_acc = BankAccount("Muhammad Bitar", 123)
# print(bitar_acc.full_name)
# print(bitar_acc.account_num)
# bitar_acc.deposit(200)
# bitar_acc.deposit(400)
# # bitar_acc.withdraw(601)
# print(bitar_acc.get_balance())

# amjad_acc = BankAccount.from_dict({
#     "account_num": 124,
#     "full_name": "Amjad Bakro"
# })
# # amjad_acc.withdraw(20)
# amjad_acc.deposit(20)

# amjad_acc = BankAccount.from_dict({
#     "account_num": "123@",
#     "full_name": "Amjad Bakro"
# })
# # amjad_acc.withdraw(20)
# amjad_acc.deposit(20)
