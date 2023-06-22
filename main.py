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


def securityCheck(*args) -> bool:
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
    def __init__(self) -> int:
        def login(cursor) -> str:
            '''
        Login command to take user input and check is it password.\n
        takes 0 args, only asks inside of function.\n
        returns customer_name and True if user input is correct
            '''
            customer_name = input("What is your name?: ").lower()
            password = getpass.getpass("What is your password?: ")

            cursor.execute(f'select customer_id from customers_table where customer_name = "{customer_name}" and customer_password = "{password}";')
            result = cursor.fetchone()

            try:  # causes bug, when everything is ok
                print(result[0])
                atma = atm(result[0]) # result[0] - customer_id
                atma.__init__()
                print("Logged in successfully")
            except Exception as err:
                print(f"Name or password is incorrect {err}")

            
        def changePassword(cursor) -> None:
            '''
        ChngPass command to take user input and set it as password.\n
        takes 0 args, only asks inside of function.
            '''
            customer_name = input("What is your name?: ").lower()

            old_password = getpass.getpass("What is your password?: ")
            new_password = getpass.getpass("What password do you want? (max: 20 chars): ")

            cursor.execute(f'select customer_id from customers_table where customer_name = "{customer_name}" and customer_password = "{old_password}";')
            result = cursor.fetchone()

            try: 
                result[0] #result[0] - customer_id: login check, if no user found - raises error, if found one - going futher
                cursor.execute(f'update customers_table set customer_password = "{new_password}" where customer_name = "{customer_name}";')
                print("Successfully changed password!")
            except Exception as err:
                print(f"Name or password is incorrect {err}")


        def register(cursor) -> None:
            '''
        Register command to take user input and load it into customers_table.\n
        takes 0 args, only asks inside of function.
            '''

            customer_name = input("What is your name? (max: 16 chars): ")
            password = getpass.getpass("What password do you want? (max: 20 chars): ")

            securityCheck(customer_name, password)

            try:
                cursor.execute(f'insert into customers_table(customer_name, customer_password) values ("{customer_name}", "{password}");')

            except Exception as err:
                print(err)

            
        def deleteAcc(cursor) -> None:
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
                cursor.execute(f'delete from customers_table where customer_id = {customer_id};')


        def main():
                '''
            Gui command to print auth menu in terminal.\n
            Takes int 1-4 to reach other commands, if input is incorrect trying again.
            '''
                while True:
                    try:
                        cursor = db.cursor()

                        match int(input('\n\n\n\n\n===ATM===\n1) Login\n2) Register\n3) Change password\n4) Delete account\n5) Exit\n')):
                            case 1: login(cursor); input("Press ENTER")
                            case 2: register(cursor); input("Press ENTER")
                            case 3: changePassword(cursor); input("Press ENTER")
                            case 4: deleteAcc(cursor); input("Press ENTER")
                            case 5: exit()
                        cursor.execute("commit;")
                        cursor.close() # to avoid out-of-sync error
                    except Exception as err: 
                        print(f'[BUG] {err}')
                    
        
        
        main()


class atm():
    def __init__(self, current_customer_id) -> None:
        def getCustomerNameById(cursor, current_customer_id):
            cursor.execute(f'select customer_name from customers_table where customer_id = {current_customer_id};')
            return cursor.fetchone()[0]
        def deposit(cursor) -> None:
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

            cursor.execute(f'update customers_table set customer_cash = customer_cash + {cash} where customer_id = "{current_customer_id}";')
            printCashAmountById(current_customer_id, cursor)


        def withdraw(cursor) -> None:
            '''
        Withdraw command to update CASH at customer_id.\n
        Cash -= cash_input for user.\n
        takes 0 args, only asks inside of function.
        '''
            try: #check how much money customer have
                cursor.execute(f'select customer_cash from customers_table where customer_id = {current_customer_id};')
                result = cursor.fetchone()
            except: pass

            try:
                cash = int(input('How much do you want to withdraw (input integer)?: '))
                if cash < 0 or int(result[0]) - cash < 0:
                    print("You cant take debt here!")
                    cash = str(cash)
                    cash = "nope"
            except:
                print("Withdraw Only integers and positive numbers, ATM can not hold cents")

            cursor.execute(f'update customers_table set customer_cash = customer_cash - {cash} where customer_id = "{current_customer_id}";')
            printCashAmountById(current_customer_id, cursor)


        def send(cursor) -> None:
            '''
        Send command to update CASH at customer_id[i] and customer_id[j].\n
        Sends cash from one user to another.\n
        takes 0 args, only asks inside of function.
        '''
            cursor.execute('select customer_name from customers_table;')
            
            for i, name in enumerate(cursor.fetchall(), start=1):
                print(f"{i}) {name}")
            try:
                taker_id = int(input('Send money to who? (taker id): '))
            except: pass

            try: #check how much money customer do have
                cursor.execute(f'select customer_cash from customers_table where customer_id = {current_customer_id};')
                cash_on_sender_card = cursor.fetchone()
            except: pass

            try:
                cash_to_send = int(input('How much do you want to withdraw (input integer)?: '))
                if cash_to_send < 0 or int(cash_on_sender_card[0]) - cash_to_send < 0:
                    print("You cant take debt here!")
                    cash_to_send = str(cash_to_send)
                    cash_to_send = "nope"
            except:
                print("Only integers and positive numbers, ATM can not hold cents")

            a = f'update customers_table set customer_cash = customer_cash - {cash_to_send} where customer_id = "{current_customer_id}";'
            b = f'update customers_table set customer_cash = customer_cash + {cash_to_send} where customer_id = "{taker_id}";'

            cursor.execute(a)
            cursor.execute(b)

            printCashAmountById(current_customer_id, cursor)
            printCashAmountById(taker_id, cursor)


        def printCashAmountById(current_customer_id, cursor) -> None:
            '''
        Select command to print in terminal\n
        Print in terminal amount of money of customer_id \n
        Takes 1 positional arg: customer_id e.g. "1"
        '''
            cursor.execute(f'select customer_cash from customers_table where customer_id = "{current_customer_id}";')

            result = cursor.fetchone()
            print(f"#{current_customer_id}'s cash is now {result[0]}")
            


        def main() -> None:
                '''
            Gui command to print atm menu in terminal.\n
            Takes int 1-4 to reach other commands, if input is incorrect trying again.
            '''
                while True:
                    try:
                        cursor = db.cursor()
                        match int(input(f'\n\n\n\n\n===ATM===\nHello, {getCustomerNameById(cursor, current_customer_id)}\n1) Deposit\n2) Withdraw\n3) Send cash\n4) Exit\n')):
                            case 1: deposit(cursor); input("Press ENTER")
                            case 2: withdraw(cursor); input("Press ENTER")
                            case 3: send(cursor); input("Press ENTER")
                            case 4: break
                        cursor.execute("commit;")
                        cursor.close()
                    except Exception as err: 
                        print(f'[BUG] {err}')
                    

        
        main()
         

if __name__ == "__main__":
    #atmRunner = atm()
    #atmRunner.__init__()
    
    accManagment = accountManagment()
    accManagment.__init__()


