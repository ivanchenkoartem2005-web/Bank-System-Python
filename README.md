# Bank Account Manager

A simple command-line bank application written in Python. Accounts are stored in a local JSON file, so your data persists between runs.

## Features

- Create accounts with an owner name, account number and starting balance
- Deposit and withdraw money
- Transfer money between accounts
- View balance and full transaction history
- Input validation: no negative or zero amounts, no overdrafts, no duplicate account numbers

## Requirements

- Python 3.8+
- No external libraries needed

## Usage

```bash
python goddamnbank.py
```

You'll see this menu:

```
1. Create account
2. Deposit
3. Withdraw
4. Transfer
5. Show balance
6. Transaction history
0. Exit
```

Most actions ask for the account number first.

## Data storage

Accounts are saved to `bank.json` in the same folder as the script. The file is created automatically on first use and is ignored by git, so no personal data gets committed.

Example record:

```json
{
    "Owner Name": "Dan_1",
    "Acc Number": 2525,
    "Balance": 6767,
    "Transfer History": ["+100$ Deposit", "-50$ Transfer to Dan_2"]
}
```

## Project structure

```
.
├── goddamnbank.py
├── .gitignore
└── README.md
```

## Notes

- This is a learning project. It has no authentication, so anyone who knows an account number can use it. Don't use it for real money.
- Balances are whole numbers only.

## License

Choose a license, for example MIT, and add a `LICENSE` file.
