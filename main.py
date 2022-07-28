from flask import Flask, request, json
import uuid
from data import Accounts, Customers, Transactions

app = Flask(__name__)


@app.route("/api/CustomerAccount/GetCustomerAccountByAccountNumber/<acc_num>", methods=["GET"])
def get_customer_account_by_account_number(acc_num):
    return {
        "body": list(filter(lambda acc: acc["Account Number"] == int(acc_num), Accounts))
    }


@app.route("/api/CustomerAccount/OpenCustomerAccount", methods=["POST"])
def open_customer_account():
    data = json.loads(request.data)
    account_num = uuid.uuid1()
    new_customer = {
        "ID": uuid.uuid1(),
        "First Name": data["First Name"],
        "Last Name": data["Last Name"],
        "Associated Account": account_num
    }
    new_account = {
        "ID": uuid.uuid1(),
        "Account Number": account_num,
        "Balance": 0,
        "Account Status": "open"
    }
    Accounts.append(new_account)
    Customers.append(new_customer)
    return {
        "body": [
            new_customer,
            new_account
        ]
    }


@app.route("/api/CustomerAccount/CloseCustomerAccount/<acc_num>", methods=["POST"])
def close_customer_account(acc_num):
    for acc in Accounts:
        if acc["Account Number"] == int(acc_num):
            acc["Account Status"] = "closed"
            return {
                "body": acc
            }
    return {
        "body": "No matching Account number"
    }


@app.route("/api/CustomerAccount/ApplyTransactionToCustomerAccountAsync", methods=["POST"])
def apply_transaction_to_customer_account_async():
    data = json.loads(request.data)
    if data["Amount"] < 0:
        return {
            "body": "Error: negative amount"
        }
    new_transaction = {
        "ID": uuid.uuid1(),
        "Amount": data["Amount"],
        "Transaction Type": data["Transaction Type"],
        "Associated Account": data["Associated Account"]
    }
    for acc in Accounts:
        if data["Associated Account"] == acc["Account Number"]:
            if data["Transaction Type"] == "debit":
                if acc["Balance"] >= data["Amount"]:
                    acc["Balance"] -= data["Amount"]
                else:
                    return {
                        "body": "Error: amount exceeds balance"
                    }
            elif data["Transaction Type"] == "credit":
                acc["Balance"] += data["Amount"]
            Transactions.append(new_transaction)
            return {
                "body": [new_transaction, acc]
            }
    return {
        "body": "No matching Account number"
    }
