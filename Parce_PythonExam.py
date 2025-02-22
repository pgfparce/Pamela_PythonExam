# Domain Layer

class Account:
    def __init__(self, account_id, customer_id, account_number, balance=0.0):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = balance
        self.transaction_history = []  

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transaction_history.append(f"Deposited: {amount}")
        return self.balance

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transaction_history.append(f"Withdraw: {amount}")
        return self.balance

    def get_balance(self):
        """Get the current balance of the account."""
        return self.balance

    def get_transaction_history(self):
        """Get the transaction history of the account."""
        return self.transaction_history


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number


# Use Case Layer

class CreateAccount:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, customer_id, name, email, phone_number):
        """Create a new account and return the Account object."""
        account_id = len(self.account_repository.accounts) + 1  
        account_number = f"ACC{account_id:05d}"
        new_account = Account(account_id, customer_id, account_number)
        self.account_repository.save_account(new_account)
        return new_account


class GenerateAccountStatement:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def generate_account_statement(self, account_id):
        """Generate an account statement for the given account ID."""
        account = self.account_repository.find_account_by_id(account_id)
        statement = f"Account ID: {account.account_id}\n"
        statement += f"Account Number: {account.account_number}\n"
        statement += f"Current Balance: {account.get_balance()}\n"
        statement += "Transaction History:\n"
        
        if account.get_transaction_history():
            for transaction in account.get_transaction_history():
                statement += f"- {transaction}\n"
        else:
            statement += "No transactions made yet.\n"
        
        return statement


# Infrastructure Layer

class AccountRepository:
    def __init__(self):
        self.accounts = []

    def save_account(self, account):
        """Save the account to the repository."""
        self.accounts.append(account)

    def find_account_by_id(self, account_id):
        """Find an account by its ID."""
        for account in self.accounts:
            if account.account_id == account_id:
                return account
        raise ValueError("Account not found.")

    def find_accounts_by_customer_id(self, customer_id):
        """Find all accounts associated with a customer ID."""
        return [account for account in self.accounts if account.customer_id == customer_id]


# Test Scenario with User Input

def main():
    # Create
    account_repository = AccountRepository()

    # Use case 
    create_account_use_case = CreateAccount(account_repository)
    generate_statement_use_case = GenerateAccountStatement(account_repository)

    while True:
        action = input("Would you like to create a new account or log in to transact? (create/login/exit): ").strip().lower()
        
        if action == 'create':
            # User input 
            customer_id = input("Enter customer ID: ")
            customer_name = input("Enter customer name: ")
            customer_email = input("Enter customer email: ")
            customer_phone = input("Enter customer phone number: ")

            # Create a new account
            account = create_account_use_case.create_account(customer_id, customer_name, customer_email, customer_phone)
            print(f"Account created: {account.account_number} with initial balance {account.get_balance()}")

            # Proceed to transaction 
            while True:
                transaction_action = input("Do you want to make a transaction? (deposit/withdraw/balance/statement/exit): ").strip().lower()
                
                if transaction_action == 'deposit':
                    amount = float(input("Enter amount to deposit: "))
                    try:
                        new_balance = account.deposit(amount)
                        print(f"New balance after deposit: {new_balance}")
                    except ValueError as e:
                        print(e)

                elif transaction_action == 'withdraw':
                    amount = float(input("Enter amount to withdraw: "))
                    try:
                        new_balance = account.withdraw(amount)
                        print(f"New balance after withdrawal: {new_balance}")
                    except ValueError as e:
                        print(e)

                elif transaction_action == 'balance':
                    print(f"Current balance: {account.get_balance()}")

                elif transaction_action == 'statement':
                    statement = generate_statement_use_case.generate_account_statement(account.account_id)
                    print(statement)

                elif transaction_action == 'exit':
                    print("Exiting transaction menu.")
                    break

                else:
                    print("Invalid input. Please enter 'deposit', 'withdraw', 'balance', 'statement', or 'exit'.")

        elif action == 'login':
            account_id = int(input("Enter your account ID to log in: "))
            try:
                account = account_repository.find_account_by_id(account_id)
                print(f"Logged in successfully. Current balance for account {account.account_number}: {account.get_balance()}")

                # Proceed to transaction 
                while True:
                    transaction_action = input("Do you want to make a transaction? (deposit/withdraw/balance/statement/exit): ").strip().lower()
                    
                    if transaction_action == 'deposit':
                        amount = float(input("Enter amount to deposit: "))
                        try:
                            new_balance = account.deposit(amount)
                            print(f"New balance after deposit: {new_balance}")
                        except ValueError as e:
                            print(e)

                    elif transaction_action == 'withdraw':
                        amount = float(input("Enter amount to withdraw: "))
                        try:
                            new_balance = account.withdraw(amount)
                            print(f"New balance after withdrawal: {new_balance}")
                        except ValueError as e:
                            print(e)

                    elif transaction_action == 'balance':
                        print(f"Current balance: {account.get_balance()}")

                    elif transaction_action == 'statement':
                        statement = generate_statement_use_case.generate_account_statement(account.account_id)
                        print(statement)

                    elif transaction_action == 'exit':
                        print("Exiting transaction menu.")
                        break

                    else:
                        print("Invalid input. Please enter 'deposit', 'withdraw', 'balance', 'statement', or 'exit'.")

            except ValueError as e:
                print(e)

        elif action == 'exit':
            print("Exiting the program.")
            break

        else:
            print("Invalid input. Please enter 'create', 'login', or 'exit'.")

if __name__ == "__main__":
    main()