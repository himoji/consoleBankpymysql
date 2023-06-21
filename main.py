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
    cursor = db.cursor()
    print("Connected successfully")

except Exception as err:
    print("Connection refused\n", err)


def securityCheck(*args) -> bool:
    '''
    Checks user input for: blacklisted words, going out-of-bounds
\n
    returns bool, True = blacklisted words are in input, False = not
    '''
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
            return True
        if word.lower() in blacklisted_words:
            return True


class accountManagment:
    def __init__(self) -> int:
        def login() -> str:
            '''
        Login command to take user input and check is it password.\n
        takes 0 args, only asks inside of function.\n
        returns customer_name and True if user input is correct
            '''
            customer_name = input("What is your name?: ").lower()
            password = getpass.getpass("What is your password?: ")

            if securityCheck(customer_name, password):
                print("Security violated!")
                exit()

            cursor.execute(f'select customer_id from customers_table where customer_name = "{customer_name}" and customer_password = "{password}";')
            result = cursor.fetchone()

            try: 
                atma = atm(result[0])
                atma.__init__()
                print("Logged in successfully")
            except Exception as err:
                print(f"Name or password is incorrect {err}")


        def register() -> None:
            '''
        Register command to take user input and load it into customers_table.\n
        takes 0 args, only asks inside of function.
            '''

            customer_name = input("What is your name? (max: 16 chars): ")
            password = getpass.getpass("What password do you want? (max: 20 chars): ")

            if securityCheck(customer_name, password):
                print("Security violated!")
                exit()

            try:
                cursor.execute(f'insert into customers_table(customer_name, customer_password) values ("{customer_name}", "{password}");commit;')

            except Exception as err:
                print(err)
            
        def deleteAcc() -> None:
            '''
        Delete command to delete a row with specified id \n
        takes 0 args, only asks inside of function.
            '''
            try:
                customer_id = int(input("What is your id?: "))
                sure = bool(int(input("Are you sure? (1 or 0)?: ")) == 1)

            except Exception as err:
                print(err)

            if sure:
                cursor.execute(f'delete from customers_table where customer_id = {customer_id};commit;')
        def main():
                '''
            Gui command to print auth menu in terminal.\n
            Takes int 1-4 to reach other commands, if input is incorrect trying again.
            '''
                while True:
                    try:
                        match int(input('\n\n\n\n\n===ATM===\n1) Login\n2) Register\n3) Delete account\n4) Exit\n')):
                            case 1: login(); input("Press ENTER")
                            case 2: register(); input("Press ENTER")
                            case 3: deleteAcc(); input("Press ENTER")
                            case 4: exit()
                    except Exception as err: 
                        print(f'[BUG] {err}')
                    cursor.execute("commit;")
        main()


class atm():
    def __init__(self, customer_id) -> None:
        def deposit() -> None:
            '''
        'Deposit command to update CASH at customer_id.\n
        Cash += cash_input for user.\n
        takes 0 args, only asks inside of function.
        '''
            try:
                cash = abs(int(input('How much do you want to deposit (input integer)?: ')))
            except:
                print("Deposit Only integers and positive numbers, ATM can not hold cents")

            cursor.execute(f'update customers_table set customer_cash = customer_cash + {cash} where customer_id = "{customer_id}";')
            printCashAmount(customer_id)


        def withdraw() -> None:
            '''
        Withdraw command to update CASH at customer_id.\n
        Cash -= cash_input for user.\n
        takes 0 args, only asks inside of function.
        '''
            try:
                cash = abs(int(input('How much do you want to withdraw (input integer)?: ')))
            except:
                print("Withdraw Only integers and positive numbers, ATM can not hold cents")

            cursor.execute(f'update customers_table set customer_cash = customer_cash - {cash} where customer_id = "{customer_id}";')
            printCashAmount(customer_id)


        def send() -> None:
            '''
        Send command to update CASH at customer_id[i] and customer_id[j].\n
        Sends cash from one user to another.\n
        takes 0 args, only asks inside of function.
        '''

            taker = input('Send money to who? (taker name): ').lower()

            try:
                cash = abs(int(input('How much do you want to withdraw (input integer)?: ')))
            except:
                print("Only integers and positive numbers, ATM can not hold cents")

            a = f'update customers_table set customer_cash = customer_cash - {cash} where customer_id = "{customer_id}";'
            b = f'update customers_table set customer_cash = customer_cash + {cash} where customer_name = "{taker}";'

            if securityCheck(taker):
                print("Security violated!")
                exit()

            cursor.execute(a)
            cursor.execute(b)

            printCashAmount(customer_id)
            #printCashAmount for customer_name
            cursor.execute(f'select customer_cash from customers_table where customer_name = "{taker}";')
            result = cursor.fetchone()
            print(f"{taker.title()}'s cash is now {result[0]}")


        def printCashAmount(customer_id) -> None:
            '''
        Select command to print in terminal\n
        Print in terminal amount of money of customer_id \n
        Takes 1 positional arg: customer_id e.g. "1"
        '''
            cursor.execute(f'select customer_cash from customers_table where customer_id = "{customer_id}";')

            result = cursor.fetchone()
            print(f"#{customer_id}'s cash is now {result[0]}")


        def main() -> None:
                '''
            Gui command to print atm menu in terminal.\n
            Takes int 1-4 to reach other commands, if input is incorrect trying again.
            '''
                while True:
                    try:
                        match int(input(f'\n\n\n\n\n===ATM===\nHello, #{customer_id}\n1) Deposit\n2) Withdraw\n3) Send cash\n4) Exit\n')):
                            case 1: deposit(); input("Press ENTER")
                            case 2: withdraw(); input("Press ENTER")
                            case 3: send(); input("Press ENTER")
                            case 4: exit() # causes bug so user need to type 4 two times
                    except Exception as err: 
                        print(f'[BUG] {err}') # causes bug
                    cursor.execute("commit;")

        
        main()
         

if __name__ == "__main__":
    #atmRunner = atm()
    #atmRunner.__init__()
    
    accManagment = accountManagment()
    accManagment.__init__()


