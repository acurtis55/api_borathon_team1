from flask import Flask, request, json
import uuid
from data import Accounts, Customers, Transactions
from db import DB

app = Flask(__name__)
db = DB()


@app.route("/api/CustomerAccount/GetCustomerAccountByAccountNumber/<acc_num>", methods=["GET"])
def get_customer_account_by_account_number(acc_num):
    return {
        "body": db.exec(f"""SELECT first_name, last_name FROM customers WHERE associated_account='{acc_num}'""")
    }


@app.route("/api/CustomerAccount/OpenCustomerAccount", methods=["POST"])
def open_customer_account():
    data = json.loads(request.data)
    account_num = uuid.uuid1()
    db.exec(f"""INSERT INTO accounts (account_number, balance, account_status)
        VALUES ('{account_num}', 0.00, 'open')""")
    db.exec(f"""INSERT INTO customers (first_name, last_name, associated_account) 
        VALUES ('{data["First Name"]}', '{data["Last Name"]}', '{account_num}')""")
    return {
        "body": [
            db.exec(f"""SELECT account_number, balance, account_status 
                FROM accounts WHERE account_number='{account_num}'"""),
            db.exec(f"""SELECT first_name, last_name, associated_account 
                FROM customers WHERE associated_account='{account_num}'""")
        ]
    }


@app.route("/api/CustomerAccount/CloseCustomerAccount", methods=["POST"])
def close_customer_account():
    data = json.loads(request.data)
    db.exec(f"""UPDATE accounts SET account_status = 'closed' WHERE account_number='{data["Associated Account"]}'""")
    return {
        "body": db.exec(f"""SELECT account_number, balance, account_status 
            FROM accounts WHERE account_number='{data["Associated Account"]}'""")
    }


@app.route("/api/CustomerAccount/ApplyTransactionToCustomerAccountAsync", methods=["POST"])
def apply_transaction_to_customer_account_async():
    data = json.loads(request.data)
    if data["Amount"] < 0:
        return {
            "body": "Error: negative amount"
        }
    acc = db.exec(f"""SELECT account_number, balance, account_status 
        FROM accounts WHERE account_number='{data["Associated Account"]}'""")
    if len(acc) != 0:
        new_balance = acc[0][1]
        if data["Transaction Type"] == "debit":
            if new_balance >= data["Amount"]:
                new_balance -= data["Amount"]
            else:
                return {
                    "body": "Error: amount exceeds balance"
                }
        elif data["Transaction Type"] == "credit":
            new_balance += data["Amount"]
        db.exec(f"""UPDATE accounts SET balance = {new_balance} WHERE account_number='{data["Associated Account"]}'""")
        db.exec(f"""INSERT INTO transactions (amount, transaction_type, associated_account) 
            VALUES ({data["Amount"]}, '{data["Transaction Type"]}', '{data["Associated Account"]}')""")
        return {
            "body": [
                db.exec(f"""SELECT account_number, balance, account_status 
                    FROM accounts WHERE account_number='{data["Associated Account"]}'"""),
                db.exec(f"""SELECT amount, transaction_type, associated_account 
                            FROM transactions WHERE associated_account='{data["Associated Account"]}'"""),
            ]
        }
    return {
        "body": "No matching Account number"
    }
