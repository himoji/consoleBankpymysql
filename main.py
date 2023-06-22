'''
Simple console-based ATM programm
with mysql database
poor perfomance, but anyway its iobound
'''



'''
TODO: loan system
check when send money
'''
#import mysql driver and connect to database with (host, user, password and database name) info
import mysql.connector
import getpass

try:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'admin',
        database = 'customers_db'
    )
    #cursor = db.cursor()
    print("Connected successfully")

except Exception as err:
    print("Connection refused\n", err)


def securityCheck(*args) -> None:
    '''
    Checks user input for: blacklisted words, going out-of-bounds
\n
    returns bool, True = blacklisted words are in input, False = not
    '''
    violated = False
    blacklisted_words = [
        "select",
        "drop",
        "delete",
        "where",
        "insert",
        "commit",
        "rollback",
        ";"
        "from",
        "*",
        "update",
        "()"
                         ]
    
    for word in args:
        if len(word) > 20: 
            violated = True

        if word.lower() in blacklisted_words:
            violated = True

    if violated:
        print("Security violated!")
        exit()


class accountManagment:
    def __init__(self) -> None:
        self.main()
    def login(self) -> None:
        '''
    Login command to take user input and check is it password.\n
    takes 0 args, only asks inside of function.\n
    returns customer_name and True if user input is correct
        '''
        customer_name = input("What is your name?: ").lower()
        password = getpass.getpass("What is your password?: ")

        self.cursor.execute(f'select customer_id from customers_table where customer_name = "{customer_name}" and customer_password = "{password}";')
        result = self.cursor.fetchone()

        try:  # causes bug, when everything is ok
            print(result[0]) #type: ignore
            print("Logged in successfully")
            atma = atm(result[0]) # type: ignore result[0] - customer_id
            atma.__init__(result[0]) # type: ignore

        except Exception as err:
            print(f"Name or password is incorrect {err}")

        
    def changePassword(self) -> None:
        '''
    ChngPass command to take user input and set it as password.\n
    takes 0 args, only asks inside of function.
        '''
        customer_name = input("What is your name?: ").lower()

        old_password = getpass.getpass("What is your password?: ")
        new_password = getpass.getpass("What password do you want? (max: 20 chars): ")

        self.cursor.execute(f'select customer_id from customers_table where customer_name = "{customer_name}" and customer_password = "{old_password}";')
        result = self.cursor.fetchone()

        try: 
            result[0] #result[0] - customer_id: login check, if no user found - raises error, if found one - going futher
            self.cursor.execute(f'update customers_table set customer_password = "{new_password}" where customer_name = "{customer_name}";')
            print("Successfully changed password!")
        except Exception as err:
            print(f"Name or password is incorrect {err}")


    def register(self) -> None:
        '''
    Register command to take user input and load it into customers_table.\n
    takes 0 args, only asks inside of function.
        '''

        customer_name = input("What is your name? (max: 16 chars): ")
        password = getpass.getpass("What password do you want? (max: 20 chars): ")

        securityCheck(customer_name, password)

        try:
            self.cursor.execute(f'insert into customers_table(customer_name, customer_password) values ("{customer_name}", "{password}");')

        except Exception as err:
            print(err)

        
    def deleteAcc(self) -> None:
        '''
    Delete command to delete a row with specified id \n
    takes 0 args, only asks inside of function.
        '''
        try:
            customer_id = int(input("What is your id?: "))
            sure = bool(int(input("Are you sure? (1 or 0)?: ")) == 1)

        except Exception as err:
            print(err)

        if sure: #type: ignore
            self.cursor.execute(f'delete from customers_table where customer_id = {customer_id};') #type: ignore


    def main(self) -> None:
            '''
        Gui command to print auth menu in terminal.\n
        Takes int 1-4 to reach other commands, if input is incorrect trying again.
        '''
            while True:
                try:
                    self.cursor = db.cursor()

                    match int(input('\n\n\n\n\n===ATM===\n1) Login\n2) Register\n3) Change password\n4) Delete account\n5) Exit\n')):
                        case 1: self.login(); input("Press ENTER")
                        case 2: self.register(); input("Press ENTER")
                        case 3: self.changePassword(); input("Press ENTER")
                        case 4: self.deleteAcc(); input("Press ENTER")
                        case 5: exit()
                    self.cursor.execute("commit;")
                    self.cursor.close() # to avoid out-of-sync error
                except Exception as err: 
                    print(f'[BUG] {err}')


class atm():
    def __init__(self, current_customer_id) -> None:
        self.current_customer_id = current_customer_id
        self.main()


    def getCustomerNameById(self):
        self.cursor.execute(f'select customer_name from customers_table where customer_id = {self.current_customer_id};')
        return self.cursor.fetchone()[0]
    

    def deposit(self) -> None:
        '''
    'Deposit command to update CASH at customer_id.\n
    Cash += cash_input for user.\n
    takes 0 args, only asks inside of function.
    '''
        try:
            cash = int(input('How much do you want to deposit (input integer)?: '))
            if cash < 0:
                print("You cant take debt here!")
                cash = str(cash)
                cash = "nope"
        except:
            print("Deposit Only integers and positive numbers, ATM can not hold cents")

        self.cursor.execute(f'update customers_table set customer_cash = customer_cash + {cash} where customer_id = "{self.current_customer_id}";') # type: ignore
        self.printCashAmount()


    def withdraw(self) -> None:
        '''
    Withdraw command to update CASH at customer_id.\n
    Cash -= cash_input for user.\n
    takes 0 args, only asks inside of function.
    '''
        try: #check how much money customer have
            self.cursor.execute(f'select customer_cash from customers_table where customer_id = {self.current_customer_id};')
            result = self.cursor.fetchone()
        except: pass

        try:
            cash = int(input('How much do you want to withdraw (input integer)?: '))
            if cash < 0 or int(result[0]) - cash < 0: #type: ignore
                print("You cant take debt here!")
                cash = str(cash)
                cash = "nope"
        except:
            print("Withdraw Only integers and positive numbers, ATM can not hold cents")

        self.cursor.execute(f'update customers_table set customer_cash = customer_cash - {cash} where customer_id = "{self.current_customer_id}";') #type: ignore
        self.printCashAmount()


    def send(self) -> None:
        '''
    Send command to update CASH at customer_id[i] and customer_id[j].\n
    Sends cash from one user to another.\n
    takes 0 args, only asks inside of function.
    '''
        self.cursor.execute('select customer_name from customers_table;')
        
        for i, name in enumerate(self.cursor.fetchall(), start=1):
            print(f"{i}) {name}")
        try:
            taker_id = int(input('Send money to who? (taker id): '))
        except: pass

        try: #check how much money customer do have
            self.cursor.execute(f'select customer_cash from customers_table where customer_id = {self.current_customer_id};')
            cash_on_sender_card = self.cursor.fetchone()
        except: pass

        try:
            cash_to_send = int(input('How much do you want to withdraw (input integer)?: '))
            if cash_to_send < 0 or int(cash_on_sender_card[0]) - cash_to_send < 0: #type: ignore
                print("You cant take debt here!")
                cash_to_send = str(cash_to_send)
                cash_to_send = "nope"
        except:
            print("Only integers and positive numbers, ATM can not hold cents")

        a = f'update customers_table set customer_cash = customer_cash - {cash_to_send} where customer_id = "{self.current_customer_id}";' # type: ignore
        b = f'update customers_table set customer_cash = customer_cash + {cash_to_send} where customer_id = "{taker_id}";' # type: ignore

        self.cursor.execute(a)
        self.cursor.execute(b)

        self.printCashAmount()
        self.printCashAmountById(taker_id) #type: ignore


    def printCashAmountById(self, current_customer_id) -> None:
        '''
    Select command to print in terminal\n
    Print in terminal amount of money of customer_id \n
    Takes 1 positional arg: customer_id e.g. "1"
    '''
        self.cursor.execute(f'select customer_cash from customers_table where customer_id = "{current_customer_id}";')

        result = self.cursor.fetchone()
        print(f"#{current_customer_id}'s cash is now {result[0]}")
        

    def printCashAmount(self) -> None:
        '''
    Select command to print in terminal\n
    Print in terminal amount of money of customer_id \n
    Takes 1 positional arg: customer_id e.g. "1"
    '''
        self.cursor.execute(f'select customer_cash from customers_table where customer_id = "{self.current_customer_id}";')

        result = self.cursor.fetchone()
        print(f"#{self.current_customer_id}'s cash is now {result[0]}")
        

    def main(self) -> None:
            '''
        Gui command to print atm menu in terminal.\n
        Takes int 1-4 to reach other commands, if input is incorrect trying again.
        '''
            while True:
                try:
                    self.cursor = db.cursor()
                    match int(input(f'\n\n\n\n\n===ATM===\nHello, {self.getCustomerNameById()}\n1) Deposit\n2) Withdraw\n3) Send cash\n4) Exit\n')):
                        case 1: self.deposit(); input("Press ENTER")
                        case 2: self.withdraw(); input("Press ENTER")
                        case 3: self.send(); input("Press ENTER")
                        case 4: break
                    self.cursor.execute("commit;")
                    self.cursor.close()
                except Exception as err: 
                    print(f'[BUG] {err}')
         

if __name__ == "__main__":
    #atmRunner = atm()
    #atmRunner.__init__()
    
    accManagment = accountManagment()
    accManagment.__init__()


