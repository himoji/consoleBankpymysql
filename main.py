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
            cash = int(input('How much do you want to deposit (input integer)?: '))

            cursor.execute(f'update customers_table set customer_cash = customer_cash + {cash} where customer_name = "{customer_name}";')
            print(f'update customers_table set customer_cash = customer_cash + {cash} where customer_name = "{customer_name}";')


        def withdraw() -> None:
            '''
        Withdraw command to update CASH at CUSTOMER_NAME.
        Cash -= cash_input for user.
        takes 0 args, only asks inside of function.
        '''

            customer_name = input('Who are you (your name)?: ')
            cash = int(input('How much do you want to withdraw (input integer)?: '))

            cursor.execute(f'update customers_table set customer_cash = customer_cash - {cash} where customer_name = "{customer_name}";')
            #print(cursor.execute(f'select customer_cash from customers_table where customer_name = "{customer_name}";'))


        def send() -> None:
            '''
        Send command to update CASH at CUSTOMER_NAME[i] and CUSTOMER_NAME[j].
        Sends cash from one user to another.
        takes 0 args, only asks inside of function.
        '''

            sender = input('Who are you (your name)?: ')
            taker = input('Send money to who? (taker name): ')
            cash = int(input('How much do you want to withdraw (input integer)?: '))

            cursor.execute(f'update customers_table set customer_cash = customer_cash - {cash} where customer_name = "{sender}";')
            cursor.execute(f'update customers_table set customer_cash = customer_cash + {cash} where customer_name = "1{taker}";')
            #print(cursor.execute(f'select customer_cash from customers_table where customer_name = "{sender}";'), cursor.execute(f'select customer_cash from customers where customer_name = "{taker}";'))


        """def selectXfromY(x, y):
            '''
        Select command to print in terminal
        Takes 2 positional args: x - what, y - out where
        '''

            cursor.execute(f'select {x} from {y}')

            result = cursor.fetchall()
            for i in result:
                print(i)"""


        def main() -> None:
                '''
            Gui command to print atm menu in terminal.
            Takes int 1-4 to reach other commands, if input is incorrect trying again.
            '''
                while True:
                    try:
                        match int(input('\n\n\n\n\n===ATM===\n1) Deposit\n2) Withdraw\n3) Send cash\n4) Exit\n')):
                            case 1: deposit()
                            case 2: withdraw()
                            case 3: send()
                            case 4: break # causes bug so user need to type 4 two times
                            case _: print('Please enter only numbers from 1 to 4: ')
                        cursor.execute("commit;")
                    except: 
                        print('Please enter only numbers (1-4): ')
        main()
         

if __name__ == "__main__":
    atmRunner = atm()
    atmRunner.__init__()


