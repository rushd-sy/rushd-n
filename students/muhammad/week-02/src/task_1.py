class BankAccount():

    def __init__(self, first_name: str, last_name: str, initial_balance: float = 0) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.__balance = initial_balance
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



my_account: BankAccount = BankAccount("Muhammad", "Bitar", 20)
print(my_account.get_balance())
my_account.withdraw(10)
my_account.deposit(20)
my_account.withdraw(100)
