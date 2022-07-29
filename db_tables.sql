
CREATE TYPE acc_status AS ENUM ('open', 'closed');
CREATE TYPE tran_type AS ENUM ('debit', 'credit');

CREATE TABLE IF NOT EXISTS Accounts(
    account_id serial PRIMARY KEY,
    account_number VARCHAR (255) UNIQUE NOT NULL,
    balance NUMERIC(1000, 2) NOT NULL,
    account_status acc_status NOT NULL
);

CREATE TABLE IF NOT EXISTS Customers(
    customer_id serial PRIMARY KEY,
    first_name VARCHAR (255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    associated_account VARCHAR (255) NOT NULL,
    FOREIGN KEY (associated_account) REFERENCES Accounts (account_number)
);

CREATE TABLE IF NOT EXISTS Transactions(
    transactions_id serial PRIMARY KEY,
    amount NUMERIC(1000, 2) NOT NULL,
    transaction_type tran_type NOT NULL,
    associated_account VARCHAR (255) NOT NULL,
    FOREIGN KEY (associated_account) REFERENCES Accounts (account_number)
);

INSERT INTO Accounts(account_number, balance, account_status)
VALUES ('297473be-0f6e-11ed-a6e5-8ae4f70d17db', 12000.00, 'open');

INSERT INTO Customers(first_name, last_name, associated_account)
VALUES ('Don', 'Joe', '297473be-0f6e-11ed-a6e5-8ae4f70d17db');

INSERT INTO Transactions(amount, transaction_type, associated_account)
VALUES (2300.00, 'debit', '297473be-0f6e-11ed-a6e5-8ae4f70d17db');