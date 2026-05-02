class BankAccount:
    balance = 0

    def deposit(self, amount):
        self.balance += amount
        print("Balance after deposit:", self.balance)

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print("Balance after withdrawal:", self.balance)
        else:
            print("Insufficient balance")


account = BankAccount()

account.deposit(100)
account.withdraw(50)