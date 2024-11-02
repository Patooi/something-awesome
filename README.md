# something-awesome

## Password Manager

This project is a simple password manager that uses bcrypt and AES to hash and encrypt your passwords. Sqlite3 is used for data storage.
The main problem people have is that the password manager is that it is a single point of failure, your master-password being the entry
point. The premise of this password-manager is that your master-password is never stored in the database, instead it is used to generate
a key to encrypt and decrypt your data.

## Prerequisites

- Python 3.6 or higher.

That's about it!

## Getting started

### Clone the repository to your local machine

```bash
git clone https://github.com/Patooi/something-awesome.git
```

### Navigate to the project directory

```bash
cd something-awesome
```

### Download the pip requirements

```bash

pip install -r requirements.txt
```

### Run the application

```bash
python3 password-manager.py
```

### Usage

1. Create an account
2. Add and delete your passwords.
