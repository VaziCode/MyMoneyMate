import logging
import uuid
import random
import json
import string
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import datetime, timedelta
from collections import defaultdict
from Backend import config
from Backend.config import categories_config
import xlsxwriter
import requests

""" Database class for handling all database operations. """
class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host =      config.DB_HOST,
            database =  config.DB_DATABASE_NAME,
            user =      config.DB_USER,
            password =  config.DB_PASSWORD,
            port =  int(config.DB_PORT))
        
        self.cursor = self.connection.cursor()
    
    # ------------------------------------------------------
    # ------------------- SETs / CREATEs -------------------
    # ------------------------------------------------------

    """ Create a new user in the database. """
    def create_user(self, user_id, user_name, login_name, password, is_admin) -> str:
        ''' create user in 'users' table '''
        #validate login_name #NOTE: XXX: !NICE TO HAVE! more validation cases
        if len(login_name) < config.LOGIN_NAME_MIN_LENGTH: return None
        if len(login_name) > config.LOGIN_NAME_MAX_LENGTH: return None
        
        #set new login_name in db
        # self.cursor.execute(f"INSERT INTO users (pk_id, user_name, login_name, password, is_admin) VALUES ('{user_id}', '{user_name}', '{(login_name).lower()}', '{password}', '{is_admin}')")
        self.cursor.execute(
            "INSERT INTO users (pk_id, user_name, login_name, password, is_admin) VALUES (%s, %s, %s, %s, %s)",
            (user_id, user_name, login_name.lower(), password, is_admin)
        )
        self.connection.commit()
        
        return login_name

    """ Create a new group in the database. """
    def create_group(self, group_id, group_name):
        ''' create group in 'groups' table '''
        # self.cursor.execute(f"INSERT INTO groups (pk_id, group_name) VALUES ('{group_id}', '{group_name}')")
        self.cursor.execute(
            "INSERT INTO groups (pk_id, group_name) VALUES (%s, %s)",
            (group_id, group_name)
        )
        self.connection.commit()
    
    """ Setting a new login name for a user. """
    def set_login_name(self, user_id, login_name) -> str:
        ''' set new login_name for user_id, return None if failed, return login_name if valid '''
        #validate login_Name #NOTE: XXX: !NICE TO HAVE! more validation cases
        if len(login_name) < config.LOGIN_NAME_MIN_LENGTH: return None
        if len(login_name) > config.LOGIN_NAME_MAX_LENGTH: return None
        
        #set new login_Name in db
        # self.cursor.execute(f"UPDATE users SET login_name = '{login_name}' WHERE pk_id = {user_id}")
        self.cursor.execute(
            "UPDATE users SET login_name = %s WHERE pk_id = %s",
            (login_name, user_id)
        )
        self.connection.commit()
        
        return login_name
    
    """ Setting a new password for a user. """
    def set_password(self, user_id, password) -> str:
        ''' set new password for user_id, return None if failed, return password if valid '''
        #validate password #NOTE: XXX: !NICE TO HAVE! more validation cases
        if len(password) < config.PASSWORD_MIN_LENGTH: return None
        if len(password) > config.PASSWORD_MAX_LENGTH: return None
        
        #set new password in db
        # self.cursor.execute(f"UPDATE users SET password = '{password}' WHERE pk_id = {user_id}")
        self.cursor.execute(
            "UPDATE users SET password = %s WHERE pk_id = %s",
            (password, user_id)
        )
        self.connection.commit()
        
        return password
    
    """ Creates usergroups row in the database. """
    def create_usergroups(self, user_id, group_id, is_group_admin) -> None:
        """ create connection (row) in 'usergroups' table """
        # Convert boolean to integer
        role_value = 1 if is_group_admin else 0
        self.cursor.execute(
            f"INSERT INTO usergroups (fk_user_id, fk_group_id, role) VALUES (%s, %s, %s)",
            (user_id, group_id, role_value)
        )
        self.connection.commit()
    
    """ Insert a new expense into the userproducts table. """
    def new_expense(self, user_id, group_id, category, price):
        """Insert a new expense into the userproducts table."""
        # Ensure the group and user exist before inserting expense
        if not self.is_group_exists(group_id):
            raise ValueError(f"Group ID {group_id} does not exist.")
        if not self.is_user_exists(user_id):
            raise ValueError(f"User ID {user_id} does not exist.")
        
        self.cursor.execute(
            "INSERT INTO userproducts (fk_user_id, fk_group_id, category_name, amount) VALUES (%s, %s, %s, %s)",
            (user_id, group_id, category, price)
        )
        self.connection.commit()
    
    # ------------------------------------------------------
    # -------------------      GETs     --------------------
    # ------------------------------------------------------
    def get_password(self, user_id) -> str:
        ''' Get password from 'users' table following given user_id '''
        #get password following given user_id
        # self.cursor.execute(f"select password from users where pk_id = {user_id}")
        self.cursor.execute(
            "SELECT password FROM users WHERE pk_id = %s",
            (user_id,)
        )
        password = self.cursor.fetchall()[0][0] #return list of tuples thats why
        if password:
            return password
        else:
            return None
        

    """ Get the login name of a user. """
    def get_login(self, user_id) -> str:
        ''' Get login_name from 'users' table following given user_id '''
        #get login_name following given user_id
        # self.cursor.execute(f"select login_name from users where pk_id = {user_id}")
        self.cursor.execute(
            "SELECT login_name FROM users WHERE pk_id = %s",
            (user_id,)
        )
        login_name = self.cursor.fetchall()[0][0] #return list of tuples thats why
        if login_name:
            return login_name
        else:
            return None
    
    """ Get the expenses of a user in a group. """
    def get_expenses(self, user_id, group_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT pk_id, date_created, fk_user_id, category_name, amount
            FROM userproducts
            WHERE fk_user_id = %s AND fk_group_id = %s
            ORDER BY date_created DESC;
        """, (user_id, group_id))
        return cursor.fetchall()
    
    # ------------------------------------------------------
    # -------------------  Is Exist -----------------------
    # -----------------------------------------------------
    """ Check if a user exists in the database. """
    def is_user_exists(self, user_id):
        ''' Check if user exists.\n
            Return (True, string of the details about the user) if exists,\n
            Return (False, None) if not exists'''
            
        #check if user_id exists
        # self.cursor.execute(f"select * from users where pk_id = {user_id}")
        self.cursor.execute(
            "SELECT * FROM users WHERE pk_id = %s",
            (user_id,)
        )
        user = self.cursor.fetchall() #return list of tuples
        if user:
            return True, user
        else:
            #create random username
            #new_user_name = generate_random_username()
            #self.add_user(user_id,user_name, new_user_name)
            return False, None
    
    """ Check if a usergroup exists in the database. """
    def is_usergroups_row_exists(self, user_id, group_id) -> bool:
        ''' return True if user-group row is already exists '''
        # self.cursor.execute(f"SELECT * FROM usergroups WHERE fk_user_id = {user_id} AND fk_group_id = {group_id}")
        self.cursor.execute(
            "SELECT * FROM usergroups WHERE fk_user_id = %s AND fk_group_id = %s",
            (user_id, group_id)
        )
        row = self.cursor.fetchall() #return list of tuples
        if row:
            return True
        else:
            return False
    
    """Check if a group exists in the database."""
    def is_group_exists(self, group_id):
        ''' Check if group exists, return True / False'''
        #check if group_id exists
        # self.cursor.execute(f"select * from groups where pk_id = {group_id}")
        self.cursor.execute(
            "SELECT * FROM groups WHERE pk_id = %s",
            (group_id,)
        )
        group = self.cursor.fetchall() #return list of tuples
        if group:
            return True
        else:
            return False
        
    """ Generic existing check method """
    def is_exists(self, user_id, user_name, group_id, group_name, group_admin_flag: bool= False, update=None):
        """ activate on report. check if user, group and usergroups exists - else create them for tracking the report """

        #check if user exists
        if not self.is_user_exists(user_id):
            #if not create random user
            while True:
                login_name = generate_random_username().lower()
                # self.cursor.execute(f"select * from users where login_name = '{login_name}'") #make sure login_name not exists
                self.cursor.execute("select * from users where login_name = %s",(login_name)) #make sure login_name not exists
                user = self.cursor.fetchall()
                if not user:
                    break
            temp_password = f"{uuid.uuid4()}" #generate new password
            self.create_user(user_id, user_name, login_name, temp_password, is_admin=0)

        # check if group exists
        if not self.is_group_exists(group_id):
            self.create_group(group_id=group_id, group_name=group_name)

        # check if user-group connection exists:
        if not self.is_usergroups_row_exists(user_id,group_id):
            self.create_usergroups(user_id=user_id, group_id=group_id, is_group_admin=1)
    
    
    """ Check if a category exists in the categories or userproducts table. """
    def is_category_exists(self, category_name: str) -> bool:
        """Check if a category already exists in the categories or userproducts table."""
        query = """
            SELECT 1 FROM categories WHERE category_name = %s
            UNION
            SELECT 1 FROM userproducts WHERE category_name = %s
            LIMIT 1
        """
        result = self.execute_query(query, (category_name, category_name))
        return result is not None
    
    # ------------------------------------------------------
    # -------------------  Other Methods -------------------
    # -----------------------------------------------------
    
    
    """ Delete an expense from the userproducts table. """
    def delete_expense(self, expense_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            DELETE FROM userproducts WHERE pk_id = %s;
        """, (expense_id,))
        
        # Commit the transaction to apply the changes
        self.connection.commit()
        
        # Check if the row was deleted
        if cursor.rowcount == 0:
            return False  # No row found with the provided pk_id
        return True  # Row successfully deleted
    
    
    """ Delete a category from the categories table. """
    def delete_category(self, category_name):
        try:
            with self.connection.cursor() as cursor:
                # Use cursor.execute, not cursor() (which would throw the TypeError)
                cursor.execute(
                    "DELETE FROM categories WHERE category_name = %s RETURNING category_name",
                    (category_name,)
                )
                result = cursor.fetchone()
                # Commit the transaction if a category was deleted
                if result:
                    self.connection.commit()
                    return True  # Indicate successful deletion
                return False  # Indicate that the category wasn't found
        except Exception as e:
            # Handle any errors and log them if needed
            logging.error(f"Error in delete_category: {e}")
            self.connection.rollback()  # Rollback in case of an error
            return False
        

    """ Export expenses to an Excel file. """
    def toExcel(self, group_id):
        # Retrieve all expenses for the group with user_name instead of user_id
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT up.pk_id, up.date_created, u.user_name, up.category_name, up.amount
            FROM userproducts up
            JOIN users u ON up.fk_user_id = u.pk_id
            WHERE up.fk_group_id = %s
            ORDER BY up.date_created DESC;
        """, (group_id,))
        expenses = cursor.fetchall()
        
        # Create an Excel file and add data
        workbook = xlsxwriter.Workbook('expenses.xlsx')
        worksheet = workbook.add_worksheet("Expenses")
        
        # Define headers for columns including Expense ID and Date
        headers = ["Expense ID", "Date", "User", "Category", "Price"]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        
        # Populate the worksheet with data
        for row_num, expense in enumerate(expenses, start=1):
            worksheet.write(row_num, 0, expense[0])  # Expense ID
            worksheet.write(row_num, 1, str(expense[1]))  # Date
            worksheet.write(row_num, 2, expense[2])  # User Name
            worksheet.write(row_num, 3, expense[3])  # Category
            worksheet.write(row_num, 4, expense[4])  # Price
        
        workbook.close()

    """ Get a pie chart of expenses for a group. """
    def piechart(self, group_id, date,currency="NIS"):
        try:
            # Define SQL query based on the date parameter
            # if date == "This Month":
            #     query = f"SELECT category_name, SUM(amount) FROM userproducts WHERE fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY category_name"
            # elif date == "Last Month":
            #     query = f"SELECT category_name, SUM(amount) FROM userproducts WHERE fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) - 1 AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY category_name"
            # else:
            #     query = f"SELECT category_name, SUM(amount) FROM userproducts WHERE fk_group_id = {group_id} GROUP BY category_name"
            if date == "This Month":
                query = """
                    SELECT category_name, SUM(amount)
                    FROM userproducts
                    WHERE fk_group_id = %s
                    AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE)
                    AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)
                    GROUP BY category_name
                """
            elif date == "Last Month":
                query = """
                    SELECT category_name, SUM(amount)
                    FROM userproducts
                    WHERE fk_group_id = %s
                    AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) - 1
                    AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)
                    GROUP BY category_name
                """
            else:
                query = """
                    SELECT category_name, SUM(amount)
                    FROM userproducts
                    WHERE fk_group_id = %s
                    GROUP BY category_name
                """
            self.cursor.execute(query, (group_id,))
            data = self.cursor.fetchall()

            # Validate that we have positive values in prices for plotting
            categories = []
            prices = []
            for row in data:
                if row[1] > 0:  # Only include positive amounts
                    categories.append(row[0])
                    prices.append(row[1])

            # If no valid positive data, skip chart generation
            if not prices:
                print("No positive expense data found for pie chart.")
                return False

            # Generate and save the pie chart
            plt.pie(prices, labels=categories, autopct='%1.1f%%')
            plt.axis('equal')
            plt.title('Expenses')
            plt.savefig('my_plot.png')
            plt.clf()
            return True  # Chart generation successful

        except Exception as e:
            logging.error(f"Error generating pie chart: {e}")
            return False

    """ Get a bar chart of expenses for a group. """
    def barchart(self,group_id, date, currency="NIS"):
        # if date == "This Month":
        #     query = f"select u.user_name, sum(amount) from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} AND EXTRACT(MONTH FROM up.date_created) = EXTRACT(MONTH FROM CURRENT_DATE) group by u.user_name"
        # elif date == "Last Month":
        #     query = f"select u.user_name, sum(amount) from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} AND EXTRACT(MONTH FROM up.date_created) = EXTRACT(MONTH FROM CURRENT_DATE) -1 group by u.user_name"
        # else:
        #     query = f"select u.user_name, sum(amount) from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} group by u.user_name"
        #
        # self.cursor.execute(query)
        # data = self.cursor.fetchall()
        try:
            if date == "This Month":
                query = """
                    SELECT u.user_name, SUM(amount)
                    FROM userproducts up
                    JOIN users u ON up.fk_user_id = u.pk_id
                    WHERE fk_group_id = %s
                      AND EXTRACT(MONTH FROM up.date_created) = EXTRACT(MONTH FROM CURRENT_DATE)
                    GROUP BY u.user_name
                """
            elif date == "Last Month":
                query = """
                    SELECT u.user_name, SUM(amount)
                    FROM userproducts up
                    JOIN users u ON up.fk_user_id = u.pk_id
                    WHERE fk_group_id = %s
                      AND EXTRACT(MONTH FROM up.date_created) = EXTRACT(MONTH FROM CURRENT_DATE) - 1
                    GROUP BY u.user_name
                """
            else:
                query = """
                    SELECT u.user_name, SUM(amount)
                    FROM userproducts up
                    JOIN users u ON up.fk_user_id = u.pk_id
                    WHERE fk_group_id = %s
                    GROUP BY u.user_name
                """
            
            self.cursor.execute(query, (group_id,))
            data = self.cursor.fetchall()
            # create lists of categories and total prices
            users = [row[0][::1] for row in data]
            prices = [row[1] for row in data]
    
            plt.bar(users, prices)
            plt.xlabel('user')
            plt.ylabel('amount spend')
            plt.title('Expenses by users')
            plt.savefig('my_plot2.png')
            plt.clf()
            
        except Exception as e:
            logging.error(f"Error generating bar chart: {e}")
            return False

    """ Get the total expenses for a group. """
    def total_expenses(self, group_id, time_period, currency="NIS"):
        # Query to get total expenses in NIS for the selected period
        # if time_period == "This Month":
        #     query = f"SELECT SUM(amount) FROM userproducts WHERE fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)"
        # elif time_period == "Last Month":
        #     query = f"SELECT SUM(amount) FROM userproducts WHERE fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) - 1 AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)"
        # else:
        #     query = f"SELECT SUM(amount) FROM userproducts WHERE fk_group_id = {group_id}"
        #
        # self.cursor.execute(query)
        # result = self.cursor.fetchone()[0] or 0  # Handle no expenses case
        try:
            if time_period == "This Month":
                query = """
                    SELECT SUM(amount)
                    FROM userproducts
                    WHERE fk_group_id = %s
                      AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE)
                      AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)
                """
            elif time_period == "Last Month":
                query = """
                    SELECT SUM(amount)
                    FROM userproducts
                    WHERE fk_group_id = %s
                      AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) - 1
                      AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)
                """
            else:
                query = """
                    SELECT SUM(amount)
                    FROM userproducts
                    WHERE fk_group_id = %s
                """
            
            self.cursor.execute(query, (group_id,))
            result = self.cursor.fetchone()[0] or 0  # Handle no expenses case
            # Conversion rates (example values)
            conversion_rates = {
                "USD": 0.27,  # 1 NIS = 0.27 USD
                "Euro": 0.23,  # 1 NIS = 0.23 Euro
                "NIS": 1.0  # 1 NIS = 1 NIS
            }
    
            # Convert result to the selected currency
            result_in_currency = result * conversion_rates.get(currency, 1.0)
            return round(result_in_currency, 2)
        
        except Exception as e:
            logging.error(f"Error in total expenses: {e}")
            return False
    
    
    """ Provide the total amount each user owes and to who 'Breakeven'. """
    def brake_even(self, group_id):
        #
        # self.cursor.execute(f"select u.user_name, sum(amount)from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} group by u.user_name")
        # data = self.cursor.fetchall()
        query = """
            SELECT u.user_name, SUM(amount)
            FROM userproducts up
            JOIN users u ON up.fk_user_id = u.pk_id
            WHERE fk_group_id = %s
            GROUP BY u.user_name
        """
        self.cursor.execute(query, (group_id,))
        data = self.cursor.fetchall()
        if not data:
            return "No expenses to split"
        balances = []
        sum = 0
        average = 0
        result = ""
        # avg payment calculation for each user
        for person in data:
            sum += person[1]
        average = sum / len(data)
        # balance calculation for each user
        for person in data:
            balances.append([person[0], average - person[1]])
        for b1 in balances:
            if b1[1] > 0:
                for b2 in balances:
                    if b2[1] < 0:
                        if b1[1] <= -b2[1]: # b1 pay all his debt to b2
                            result += b1[0] + " owe " + b2[0] + " " + str(round(b1[1])) + " ₪\n"
                            b2[1] = b2[1] + b1[1]
                            b1[1] = 0
                            break
                        else: # b1 pay part of his debt to b2
                            result += b1[0] + " owe " + b2[0] + " " + str(round(-b2[1])) + " ₪\n"
                            b1[1] = b1[1] + b2[1]
                            b2[1] = 0
        return result
    
    
    """ Add a new category to the categories table. """
    def add_category(self, category_name):
        try:
            # Assuming you have a table called "categories" in your database
            query = "INSERT INTO categories (category_name) VALUES (%s)"
            cursor = self.connection.cursor()
            cursor.execute(query, (category_name,))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logging.error(f"Error adding category to database: {e}")
    # end of class
    

    """ Execute a query and return the result if exists. """
    def execute_query(self, query: str, params: tuple) -> bool:
        """Execute a query and return the result if exists."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    
    def calculate_balances(self, group_id):
        """Calculate balances for each user in the group."""
        query = """
            SELECT u.pk_id, u.user_name, SUM(ug.amount) as balance
            FROM userproducts ug
            JOIN users u ON u.pk_id = ug.fk_user_id
            WHERE ug.fk_group_id = %s
            GROUP BY u.pk_id, u.user_name
        """
        self.cursor.execute(query, (group_id,))
        return self.cursor.fetchall()


# def write_category(group_id, new_category):
#     if not open("categories.json").read(1):
#         # file is empty
#         data = {}
#     else:
#         # file is not empty, read JSON file into a dictionary
#         with open("categories.json", "r") as f:
#             try:
#                 data = json.load(f)
#             except json.decoder.JSONDecodeError:
#                 # file is not in valid JSON format
#                 data = {}
#     # add a new key-value pair with a string value to the dictionary
#
#     if group_id in data:
#         if new_category in data[group_id] or new_category in categories_config:
#             return "Category already exists!"
#         else:
#             data[group_id].append(new_category) # add new category to the group
#
#     # group not exist. add new group
#     else:
#         data[group_id] = [new_category]
#     # write the updated dictionary to the same JSON file
#     with open("categories.json", "w") as f:
#         json.dump(data, f)
#     return "Category added successfuly!"



# def get_categories(group_id):
#
#     try:
#         with open("categories.json", "r") as f:
#             data = json.load(f)
#             if group_id in data:
#                 return data[group_id]
#             return []
#     except:
#         data = {}
#         json_string = json.dumps(data)
#         with open("categories.json", "w") as f:
#             f.write(json_string)
#         return []



# def remove_category(group_id, category):
#     if not open("categories.json").read(1):
#         # file is empty
#         return "category not exist"
#     else:
#         # file is not empty, read JSON file into a dictionary
#         with open("categories.json", "r") as f:
#             try:
#                 data = json.load(f)
#             except json.decoder.JSONDecodeError:
#                 # file is not in valid JSON format
#                 return "category not exist"
#     if group_id in data:
#         if category in data[group_id]:
#             data[group_id].remove(str(category))
#             with open("categories.json", "w") as f:
#                 json.dump(data, f)
#             return "category removed successfuly!"
#     else:
#         return "category not exist"


def generate_random_username(length=8):
    """Generate a random username."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def validate_input(input):

    if not input.isnumeric():
        return "You must enter a number"

    if int(input) < 0:
        return "Expense must be greater than 0"
    
    if int(input) > 10000000:
        return "Expense must be less than 10,000,000"
