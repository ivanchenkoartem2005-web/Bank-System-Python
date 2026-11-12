import json
from pathlib import Path

BANK_FILE = Path(__file__).resolve().parent / "bank.json"


def load_bank():
    if not BANK_FILE.exists() or BANK_FILE.stat().st_size == 0:
        return []
    try:
        with BANK_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {BANK_FILE}")
        return []


def save_bank(records):
    with BANK_FILE.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)


class BankAccount:
    def __init__(self, owner_name, account_number, balance=0, transaction_history=None):
        self.owner_name = owner_name
        self.account_number = account_number
        self.balance = balance
        self.transaction_history = transaction_history or []

    @staticmethod
    def _check_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

    def deposit(self, amount):
        self._check_amount(amount)
        self.balance += amount
        self.transaction_history.append(f"+{amount}$ Deposit")

    def withdraw(self, amount):
        self._check_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transaction_history.append(f"-{amount}$ Withdraw")

    def transfer(self, other, amount):
        """Send money from this account to another account."""
        self._check_amount(amount)
        if other is self:
            raise ValueError("You cannot transfer money to the same account.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        other.balance += amount
        self.transaction_history.append(f"-{amount}$ Transfer to {other.owner_name}")
        other.transaction_history.append(f"+{amount}$ Transfer from {self.owner_name}")

    def display_balance(self):
        print(f"Hello {self.owner_name}. Your balance is {self.balance}$")

    def show_transactions(self):
        if not self.transaction_history:
            print("No transactions yet.")
        for index, item in enumerate(self.transaction_history, start=1):
            print(f"{index}. {item}")

    def to_dict(self):
        return {
            "Owner Name": self.owner_name,
            "Acc Number": self.account_number,
            "Balance": self.balance,
            "Transfer History": self.transaction_history,
        }

    @classmethod
    def from_dict(cls, record):
        return cls(
            record["Owner Name"],
            record["Acc Number"],
            record["Balance"],
            record.get("Transfer History", []),
        )


class Bank:
    def __init__(self):
        self.accounts = [BankAccount.from_dict(r) for r in load_bank()]

    def save(self):
        save_bank([acc.to_dict() for acc in self.accounts])

    def find(self, account_number):
        for acc in self.accounts:
            if acc.account_number == account_number:
                return acc
        return None

    def create_account(self, owner_name, account_number, balance=0):
        if self.find(account_number):
            raise ValueError("An account with this number already exists.")
        if balance < 0:
            raise ValueError("Starting balance cannot be negative.")
        account = BankAccount(owner_name, account_number, balance)
        self.accounts.append(account)
        self.save()
        return account


def ask_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a whole number.")
        return None


def select_account(bank, prompt):
    number = ask_int(prompt)
    if number is None:
        return None
    account = bank.find(number)
    if account is None:
        print("Account not found.")
    return account


def main():
    bank = Bank()
    menu = (
        "\n1. Create account\n2. Deposit\n3. Withdraw\n"
        "4. Transfer\n5. Show balance\n6. Transaction history\n0. Exit"
    )

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Owner name: ").strip()
                number = ask_int("Account number: ")
                balance = ask_int("Starting balance: ")
                if name and number is not None and balance is not None:
                    bank.create_account(name, number, balance)
                    print("New account has been created.")

            elif choice in ("2", "3", "5", "6"):
                account = select_account(bank, "Account number: ")
                if account is None:
                    continue
                if choice == "2":
                    amount = ask_int("Amount to deposit: ")
                    if amount is not None:
                        account.deposit(amount)
                        bank.save()
                        print(f"{amount}$ deposited.")
                elif choice == "3":
                    amount = ask_int("Amount to withdraw: ")
                    if amount is not None:
                        account.withdraw(amount)
                        bank.save()
                        print(f"{amount}$ withdrawn.")
                elif choice == "5":
                    account.display_balance()
                else:
                    account.show_transactions()

            elif choice == "4":
                sender = select_account(bank, "Your account number: ")
                receiver = select_account(bank, "Receiver account number: ") if sender else None
                amount = ask_int("Amount to transfer: ") if receiver else None
                if amount is not None:
                    sender.transfer(receiver, amount)
                    bank.save()
                    print(f"{amount}$ sent to {receiver.owner_name}.")

            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()