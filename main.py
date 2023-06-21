'''
Simple console-based ATM programm
with mysql database
'''
#import mysql driver and connect to database with (host, user, password and database_name) info
#names init

'''
TODO: customer_name is an option, no need to write name in other def
Examle:
Who are you (input integer):
1) customer_name[0]
2) customer_name[1]
3) customer_name[2]

2
'''
import mysql.connector
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'customers_db'
)
cursor = db.cursor()

class atm():
    def __init__(self) -> None:
        def deposit() -> None:
            '''
        'Deposit command to update CASH at CUSTOMER_NAME.
        Cash += cash_input for user.
        takes 0 args, only asks inside of function.
        '''

            customer_name = input('Who are you (your name)?: ')
            try:
                cash = int(input('How much do you want to deposit (input integer)?: '))
            except:
                print("Deposit only integers, ATM can not hold cents")

            cursor.execute(f'update customers_table set customer_cash = customer_cash + {cash} where customer_name = "{customer_name}";')
            printCashAmount(customer_name)


        def withdraw() -> None:
            '''
        Withdraw command to update CASH at CUSTOMER_NAME.
        Cash -= cash_input for user.
        takes 0 args, only asks inside of function.
        '''

            customer_name = input('Who are you (your name)?: ')
            try:
                cash = int(input('How much do you want to withdraw (input integer)?: '))
            except:
                print("Withdraw only integers, ATM can not hold cents")

            cursor.execute(f'update customers_table set customer_cash = customer_cash - {cash} where customer_name = "{customer_name}";')
            printCashAmount(customer_name)


        def send() -> None:
            '''
        Send command to update CASH at CUSTOMER_NAME[i] and CUSTOMER_NAME[j].
        Sends cash from one user to another.
        takes 0 args, only asks inside of function.
        '''

            sender = input('Who are you (your name)?: ')
            taker = input('Send money to who? (taker name): ')

            try:
                cash = int(input('How much do you want to withdraw (input integer)?: '))
            except:
                print("Only integers, ATM can not hold cents")

            a = f'update customers_table set customer_cash = customer_cash - {cash} where customer_name = "{sender}";'
            b = f'update customers_table set customer_cash = customer_cash + {cash} where customer_name = "{taker}";'

            cursor.execute(a)
            cursor.execute(b)

            printCashAmount(sender)
            printCashAmount(taker)


        def printCashAmount(customer_name):
            '''
        Select command to print in terminal
        Print in terminal amount of money of CUSTOMER_NAME 
        Takes 1 positional arg: customer_name e.g. Mark Robert
        '''
            cursor.execute(f'select customer_cash from customers_table where customer_name = "{customer_name}";')

            result = cursor.fetchone()
            for i in result:
                print(f"{customer_name} cash is now {i}")


        def main() -> None:
                '''
            Gui command to print atm menu in terminal.
            Takes int 1-4 to reach other commands, if input is incorrect trying again.
            '''
                while True:
                    try:
                        match int(input('\n\n\n\n\n===ATM===\n1) Deposit\n2) Withdraw\n3) Send cash\n4) Exit\n')):
                            case 1: deposit(); input("Press ENTER")
                            case 2: withdraw(); input("Press ENTER")
                            case 3: send(); input("Press ENTER")
                            case 4: break # causes bug so user need to type 4 two times
                    except Exception as err: 
                        print(f'[BUG] {err}') # causes bug
                    cursor.execute("commit;")
        main()
         

if __name__ == "__main__":
    atmRunner = atm()
    atmRunner.__init__()
