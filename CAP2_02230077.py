import random  # We should be importing the random module  
import os  # Then we should be Importing os module to check file existence 

# create Account class
class Account:
    def _init_(self, Accountnum, Password, type_of_account, remaining_balance=0):
        self.Accountnum = Accountnum  # Account number
        self.Password = Password  # For Passwords
        self.type_of_account = type_of_account  # For slecting account_type
        self.remaining_balance = float(remaining_balance)  # total account balance left.
    def deposit(self, amount):
        # Now it is the simpliest method to deposit the amount we want to put into an account
        self.remaining_balance = self.remaining_balance + amount
        print(f"Deposited Ngultrum{amount}. New remaining_balance: Ngultrum{self.remaining_balance}")
    
    def withdraw(self, amount):
        # method to withdraw the desired amount from an account
        if amount > self.remaining_balance:
            print("Insufficient funds.")# If insufficient input
        else:
            self.remaining_balance = self.remaining_balance - amount
            print(f"Withdrew Ngultrum{amount}. New remaining_balance: Ngultrum{self.remaining_balance}")
    
    def check_remaining_balance(self):
        # method to check account balance
        return self.remaining_balance

    def transfer(self, amount, recipient_account):
        # method to tansfer money
        if amount > self.remaining_balance:
            print("Insufficient funds.")
        else:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            print(f"Transferred Ngultrum{amount} to account {recipient_account.Accountnum}")

    def change_accountnumber(self, new_accountnumber):
        # to change account number, we can use this Method 
        self.Accountnum = new_accountnumber

    def change_password(self, new_password):
        # changing account passwordr using this Method 
        self.Password = new_password

# We should add the class called Business of an Account class
class BusinessAccount(Account):
    def _init_(self, Accountnum, Password, remaining_balance=0, business_name=""):
        super()._init_(Accountnum, Password, "Business", remaining_balance)
        self.business_name = business_name  # Then we should produce business name specific to BusinessAccount

# Then  We should add another class for PersonalAccount
class PersonalAccount(Account):
    def _init_(self, Accountnum, Password, remaining_balance=0, owner_name=""):
        super()._init_(Accountnum, Password, "Personal", remaining_balance)
        self.owner_name = owner_name  # We can provide an owner name specific to PersonalAccount

def SAVE_ACCOUNT(account):
    """
    We can now save the account details to file. Tne should load all accounts, and we can should update the given account,
    and write them back to file.
    """
    accounts = load_accounts()  # to check the load existing accounts from file
    accounts[account.Accountnum] = account  # Then we have access to update
    with open('accounts.txt', 'w') as f: # The function with is called to read the account.txt
        for acc in accounts.values():
            f.write(f"{acc.Accountnum},{acc.Password},{acc.type_of_account},{acc.remaining_balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")

def load_accounts():
    """
    Load all accounts from file and return them as a dictionary.
    """#To Return and store in 
    accounts = {}
    if os.path.exists('accounts.txt'):  # Checking if required files is exist in account.txt 
        with open('accounts.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')  # By using the fuction strip() and split() in order to Split line into parts
                Accountnum, Password, type_of_account, remaining_balance = parts[:4]
                remaining_balance = float(remaining_balance)
                if type_of_account == "Business": #if want to create the business purposes
                    business_name = parts[4] # Naming the account 
                    accounts[Accountnum] = BusinessAccount(Accountnum, Password, remaining_balance, business_name)
                elif type_of_account == "Personal":
                    owner_name = parts[5] #making account for personal usage
                    accounts[Accountnum] = PersonalAccount(Accountnum, Password, remaining_balance, owner_name)
    return accounts

def create_account():
    """
    Create a new account based on user input and save it to file.
    """
    Accountnum = str(random.randint(10000, 99999))  # In order to generate the random account number that once the random was called
    Password = str(random.randint(1000, 9999))  # to generate the random Password that once the random function was called
    type_of_account = input("Enter account type (Business/Personal): ") #Entering the account you want to open
    
    if type_of_account == "Business":#If we want to open the bussiness account
        business_name = input("Enter business name: ")#name of the bussiness
        account = BusinessAccount(Accountnum, Password, business_name=business_name)
    else:
        owner_name = input("Enter owner name: ")#If we want to open the personal account
        account = PersonalAccount(Accountnum, Password, owner_name=owner_name)
    #For the name of the personal account to be created
    SAVE_ACCOUNT(account)  # Now after all we can Save the new account to file that is stored in accounts.txt
    print(f"Account created! Your account number is {Accountnum} and Password is {Password}")

def login(accounts):#After creating an account we can logint the account to do digital banking works
    """
    Log in to an account by verifying the account number and Password.
    """
    Accountnum = input("Enter account number: ")
    Password = input("Enter Password: ")# Using the given account number and the Password
    
    account = accounts.get(Accountnum)
    if account and account.Password == Password:
        print(f"Welcome, {account.type_of_account} account holder!")# the given account number and Password should be matched in order to login in the account
        return account
    else:
        print("Invalid account number or Password.")# if it is incorrect, we will be redirected
        return None

def delete_account(account):#If the account is to be deleted
    """
    Delete an account from file by removing it from the accounts dictionary
    and writing the updated dictionary back to file.
    """
    accounts = load_accounts()  # In oder to delete the account we should Load existing accounts
    if account.Accountnum in accounts:
        del accounts[account.Accountnum]  # Then we can Remove the account from the stored or load existing account
        with open('accounts.txt', 'w') as f:
            for acc in accounts.values():#reading the accounts.txt  if the account is deleted
                f.write(f"{acc.Accountnum},{acc.Password},{acc.type_of_account},{acc.remaining_balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")
        print("Account deleted successfully.")# account removed seccessfully
    else:
        print("Account not found.")

def change_account_details(account):# in order to change the account number and the Password on our own
    """
    Change account details like account number or Password based on user CHOICES.
    """
    print("\n1. Change Account Number\n2. Change Password")
    CHOICES = input("Enter CHOICES: ")
    
    if CHOICES == '1':#To change the account number
        new_accountnumber = input("Enter new account number: ")#new account number to be implemmended
        accounts = load_accounts()
        if new_accountnumber in accounts:
            print("Account number already exists.")
        else:
            old_accountnumber = account.Accountnum
            account.change_accountnumber(new_accountnumber)#account number should be matched with given account number
            SAVE_ACCOUNT(account)  # then need to save the account with the new account number which was changed earlier
            if old_accountnumber in accounts:
                del accounts[old_accountnumber]  # Then we can be able to remove the old account entry
                with open('accounts.txt', 'w') as f:
                    for acc in accounts.values():#For reading the accounts.txt
                        f.write(f"{acc.Accountnum},{acc.Password},{acc.type_of_account},{acc.remaining_balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")
            print("Account number was been now changed successfully.")
    elif CHOICES == '2':
        new_password = input("Enter new Password: ")#After changing account number, if we want to change the Password, we can use following code
        account.change_password(new_password)
        SAVE_ACCOUNT(account)  # Then after Saving,  the account with the new Password is also saved
        print("Password was changed successfully.")
    else:
        print("Invalid CHOICES.")#Password given to be changed should be perfectly matched

def main():#Main function
    """
    Main function to display menu and handle user choices.
    """
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        CHOICES = input("Enter CHOICES: ")
        
        if CHOICES == '1':# Now new account is going to be produced
            create_account()
        elif CHOICES == '2':
            accounts = load_accounts()  # After the account is being produced, Load existing accounts can be opened
            account = login(accounts)
            if account:#after the account is being logged in, we can used the banking services facilities
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check remaining_balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout")
                    CHOICES = input("Enter CHOICES: ")
                    
                    if CHOICES == '1':#Now we can deposite the desired amount of money
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        SAVE_ACCOUNT(account)  # Then we should Save account after the money has been deposited
                    elif CHOICES == '2':#We can also withdraw the deposited money back
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        SAVE_ACCOUNT(account)  # As usual we should Save account after withdrawal
                    elif CHOICES == '3':#Then we can also check the remaining balance after deposition or withdrawal of money
                        print(f"remaining_balance: Ngultrum {account.check_remaining_balance()}")
                    elif CHOICES == '4':#In order to transfer the money, we should check the existing account number
                        recipient_number = input("Enter recipient account number: ")#Entering the recipent account number
                        recipient = accounts.get(recipient_number)
                        if recipient:#Recipent account number should be exactly matched
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(amount, recipient)
                            SAVE_ACCOUNT(account)  # then we should Save sender account
                            SAVE_ACCOUNT(recipient)  # And also we should Save the recipient account
                        else:
                            print("Recipient account does not exist.")#If wrong account number is entered
                    elif CHOICES == '5':
                        delete_account(account)  # We can also delete the existing account and able to exit to main menu
                        break
                    elif CHOICES == '6':#We can also change the details of the account selecting this choices
                        change_account_details(account)
                    elif CHOICES == '7':
                        SAVE_ACCOUNT(account)  # Now if we want to logout the song, the account will be Saved before logging out
                        print("Logged out.")#Logging out
                        break
        elif CHOICES == '3':#In order to exit the banking system
            break
        else:
            print("Invalid CHOICES. Try again.")#any other wrong input

if __name__ == "_main_":#Calling of the mainfunction 
    main()
