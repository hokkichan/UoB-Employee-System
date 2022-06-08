# Cloud and Database May 2022 | lab 3
import sqlite3
import os
import re

# Clear console
def clear_console():
    os.system('clear')

class DBOperations:
  # Variables for SQL commands
  sql_create_table_firsttime = "CREATE TABLE Employees (employeeId INT (3), title VARCHAR(5), forename VARCHAR(10), surname VARCHAR(10), email VARCHAR(26), salary INT (6));"

  sql_create_table = "CREATE TABLE IF NOT EXISTS Employees (employeeId INT (3), title VARCHAR(5), forename VARCHAR(10), surname VARCHAR(10), email VARCHAR(26), salary INT (6));"

  sql_insert = "INSERT INTO Employees (employeeId, title, forename, surname, email, salary) VALUES (?, ?, ?, ?, ?, ?)"
  sql_select_all = "SELECT employeeId, title, forename, surname, email, salary FROM Employees ORDER BY employeeId ASC"
  sql_search = "SELECT * FROM Employees where employeeId = "
  sql_delete_data = "DELETE FROM Employees WHERE employeeId = (?)"
  sql_drop_table = "DROP TABLE Employees"
  sql_drop_table_if_exists = "DROP TABLE IF EXISTS Employees"
  sql_test_data = [(1, 'Mr', 'Boris', 'John', 'boris.john@bath.ac.uk', 3000), (2, 'Prof', 'Alan', 'Turing', 'alan.turing@bath.ac.uk', 4500), (3, 'Miss', 'Emily', 'Brunt', 'emily.brunt@bath.ac.uk', 2800), (4, 'Mr', 'Rowan', 'Atkinson', 'rowan.atkinson@bath.ac.uk', 2000), (5, 'Mr', 'James', 'Cook', 'james.cook@bath.ac.uk', 2300), (6, 'Mr', 'Lloyd', 'George', 'lloyd.george@bath.ac.uk', 2700), (7, 'Ms', 'Jennifer', 'Lopez', 'jennifer.lopez@bath.ac.uk', 3800), (8, 'Dr', 'Charles', 'Darwin', 'charles.darwin@bath.ac.uk', 3500), (9, 'Ms', 'Taylor', 'Swift', 'taylor.swift@bath.ac.uk', 3100), (10, 'Mr', 'Justin', 'Bieber', 'justin.biber@bath.ac.uk', 2000)]

  # Check if Employees table has been created
  def bool_sql(self):
    self.get_connection()
    self.cur.execute("SELECT count(*) FROM sqlite_master WHERE name='Employees'")
    result = self.cur.fetchone()
    return result[0]

  # Validation for email format
  def validate_email(self, email):  
    regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if(re.search(regex,email)):
        return True  
    else:   
        return False
  
  # Validation for salary
  def validate_salary(self, salary):
    if salary >0:
      return True
    else:
      return False
    
  # Connect to database
  def get_connection(self):
    self.conn = sqlite3.connect("UoB_Employees.db")
    self.cur = self.conn.cursor()

  # Menu 1 - Create Employee table
  def create_table(self):
    clear_console()
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table_firsttime)
      self.conn.commit()
      print("Table created successfully")
    except Exception as e:
      print("Error:", e)
    finally:
      self.conn.close()

  # Menu 2 - Insert data into table
  def insert_data(self):
    clear_console()
    try:
      self.select_all()
      self.get_connection()
      # Create table in background if not exists
      self.cur.execute(self.sql_create_table)
      print("\nPlease enter data for the emoployee")
      try:
        emp_ID = int(input("Enter Employee ID: "))
      except:
        print("Please enter a valid integer")
        emp_ID = int(input("Enter Employee ID: "))
      emp_Title = str(input("Enter Employee Title: "))
      emp_Forename = str(input("Enter Employee Forename: "))
      emp_Surname = str(input("Enter Employee Surname: "))
      emp_Email_temp = str(input("Enter Employee Email: "))
      # Validation for email format
      while (True):
        emp_Email = emp_Email_temp
        if not self.validate_email(emp_Email_temp):
          print("Error, invalid email format")
          emp_Email_temp = str(input("Enter Employee Email: "))
          continue
        else:
          break  
      try:
        emp_Salary_temp = int(input("Enter Employee salary: "))
        # Validation for salary amount
        while (True):
          emp_Salary = emp_Salary_temp
          if not self.validate_salary(emp_Salary_temp):
            print("Please enter a positive figure")
            emp_Salary_temp = str(input("Enter a valid salary: "))
            continue
          else:
            break
      except:
        print("Please enter a valid integer")

      # Query to insert data into the table
      variable = (emp_ID, emp_Title, emp_Forename, emp_Surname, emp_Email, emp_Salary)
      self.cur.execute(self.sql_insert, variable)
      self.conn.commit()
      self.select_all()
      print("\nInserted data successfully")
    except:
      print("Error, please try again.")
    finally:
      self.conn.close()   

  # Menu 3 - Print out all data in table
  def select_all(self):
    clear_console()
    # Check if table exists
    result = self.bool_sql()
    if result == 0:
      print ("Error. Cannot find table.")
    else:
      try:
        self.get_connection()
        # Print out header
        print('{0: <5}'.format('No.'), '{0: <6}'.format('Title'), '{0: <11}'.format('Forename'),'{0: <11}'.format('Surname'),'{0: <26}'.format('Email'),'{0: <7}'.format('Salary'))
        print("----------------------------------------------------------------------")
        # Print out table content
        self.cur.execute(self.sql_select_all)
        all_rows = self.cur.fetchall()
        for row in all_rows:
          print('{0: <5} {1: <6} {2: <11} {3: <11} {4: <26} {5: <7}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
      except Exception as e:
        print(e)
      finally:
        self.conn.close()

  # Menu 4 - Search data (by Employee ID)
  def search_data(self):
    clear_console()
    result = self.bool_sql()
    if result == 0:
      print ("Error. Cannot find table.")
    else:
      try:
        self.get_connection()
        employeeID = int(input("Enter Employee ID: "))
        clear_console() 
        self.cur.execute(self.sql_search+str(employeeID))
        result = self.cur.fetchone()
        if type(result) == type(tuple()):
          for index, detail in enumerate(result):
            if index == 0:
              print("Employee ID: " + str(detail))
            elif index == 1:
              print("Employee Title: " + detail)
            elif index == 2:
              print("Employee Name: " + detail)
            elif index == 3:
              print("Employee Surname: " + detail)
            elif index == 4:
              print("Employee Email: " + detail)
            else:
              print("Salary: "+ str(detail))
        else:
          print ("No Record")
      except Exception as e:
        print(e)
      finally:
        self.conn.close()

  # Menu 5 - Update data
  def update_data(self):
    clear_console()
    result = self.bool_sql()
    if result == 0:
      print ("Error. Cannot find table.")
    else:
      #clear_console()
      self.select_all()
      try:
        self.get_connection()
        employeeID_update = int(input("\nEnter Employee ID for updating: "))
        self.cur.execute(self.sql_search+str(employeeID_update))
        result = self.cur.fetchone()
        if result is None:
          employeeID_update = int(input("\nError. Please enter a valid Employee ID for updating: "))
        else:
          employeeID_updated = int(input("\nEnter Updated Employee ID: "))
          emp_Title = str(input("Enter Updated Title: "))
          emp_Forename = str(input("Enter Updated Forename: "))
          emp_Surname = str(input("Enter Updated Surname: "))
          emp_Email_temp = str(input("Enter Employee Email: "))
          # Validation for email format
          while (True):
            emp_Email = emp_Email_temp
            if not self.validate_email(emp_Email_temp):
              print("Invalid email format")
              emp_Email_temp = str(input("Enter Employee Email: "))
              continue
            else:
              break  
          try:
            emp_Salary_temp = int(input("Enter a valid employee salary: "))
            # Validation for salary amount
            while (True):
              emp_Salary = emp_Salary_temp
              if not self.validate_salary(emp_Salary_temp):
                print("Please enter a positive figure")
                emp_Salary_temp = str(input("Enter a valid salary: "))
                continue
              else:
                break
          except:
            print("Please enter a valid integer")

          # SQL Query to update table data
          self.cur.execute("Update Employees SET employeeID = '{}', title = '{}', forename = '{}', surname = '{}', email = '{}', salary = {} WHERE employeeId = {}".format(employeeID_updated, emp_Title, emp_Forename, emp_Surname, emp_Email, emp_Salary, employeeID_update))
          self.conn.commit()
          print("Content updated\n")
          self.select_all()
      except:
        print("Error, please try again.")
      finally: 
        self.conn.close()

  # Menu 6 - Delete data
  def delete_data(self):
    clear_console()
    # Check if table exists
    result = self.bool_sql()
    if result == 0:
      print ("Error. Cannot find table.")
    else:
      print (" Menu:")
      print ("**********")
      print (" Choose mode of delete")
      print (" 1. Delete by employee ID")
      print (" 2. Delete all data")
      print (" To exit, press any key.")
      try:
        __choose_menu = int(input("Enter your choice: \n"))
        # Delete data by Employee ID
        if __choose_menu == 1:
          try:
            self.get_connection()
            employeeID_delete = int(input("Enter Employee ID: "))        
            variable = (employeeID_delete, )
            self.cur.execute(self.sql_delete_data, variable)
            result = self.cur.rowcount
            self.conn.commit()
            self.select_all()
            if result != 0:
              print (str(result)+ " Row(s) affected.")
            else:
              print ("Cannot find this record in the database")
          except Exception as e:
            print(e)
          finally: 
            self.conn.close()
        # Delete data in the table
        elif __choose_menu == 2:
          try:
            self.get_connection()
            self.cur.execute(self.sql_drop_table)
            self.conn.commit()
            print("All data deleted")
          except Exception as e:
            print(e)
          finally: 
            self.conn.close()
        else:
          print()
      except:
        print()
        
  # Menu 7 - Print out of report
  def print_report(self):
    clear_console()
    result = self.bool_sql()
    if result == 0:
      print ("Error. Cannot find table.")
    else:
      try:
        self.get_connection()
        print('{0: <5}'.format('No.'), '{0: <6}'.format('Title'), '{0: <11}'.format('Forename'),'{0: <11}'.format('Surname'),'{0: <26}'.format('Email'),'{0: <7}'.format('Salary'))
        print("----------------------------------------------------------------------")
        self.cur.execute("SELECT employeeId, title, forename, surname, email, salary FROM Employees ORDER BY salary DESC")
        all_rows = self.cur.fetchall()
        for row in all_rows:
          print('{0: <5} {1: <6} {2: <11} {3: <11} {4: <26} {5: <7}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
      except Exception as e:
        print(e)
      finally:
        self.conn.close()

  # Menu 8 - Print employee records as text file
  def print_file(self):
    clear_console()
    with open("UoB_Employees_Record.txt", "w") as f:
      try:
        self.get_connection()
        print('{0: <5}'.format('No.'), '{0: <6}'.format('Title'), '{0: <11}'.format('Forename'),'{0: <11}'.format('Surname'),'{0: <26}'.format('Email'),'{0: <7}'.format('Salary'), file=f)
        print("----------------------------------------------------------------------", file=f)
        self.cur.execute("SELECT employeeId, title, forename, surname, email, salary FROM Employees ORDER BY employeeId ASC;")
        all_rows = self.cur.fetchall()
        for row in all_rows:
          print('{0: <5} {1: <6} {2: <11} {3: <11} {4: <26} {5: <7}'.format(row[0], row[1], row[2], row[3], row[4], row[5]), file=f)
          print("----------------------------------------------------------------------", file=f)
        print ("UoB_Employees_Record.txt successfully created.")
      except:
        print("Error. Cannot find table.")
      finally:
        self.conn.close()

  # Menu 9 - Enter test data
  def insert_test_data(self):
    clear_console()
    try:
      self.get_connection()
      # Clear existing data and insert test data
      self.cur.execute(self.sql_drop_table_if_exists)
      self.cur.execute(self.sql_create_table_firsttime)
      self.cur.executemany(self.sql_insert, self.sql_test_data)
      self.conn.commit()
      # Print out test data
      self.select_all()
      print("\nCleared existed data and inserted test data successfully")
      print("\n--------------TESTING DATA ONLY PLEASE DELETE AFTER USE---------------")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# Printing of main menu
while True:
  print ("\nMenu:")
  print ("**********")
  print (" 1. Create table EmployeeUoB")
  print (" 2. Insert data into EmployeeUoB")
  print (" 3. Select all data into EmployeeUoB")
  print (" 4. Search an employee")
  print (" 5. Update data some records")
  print (" 6. Delete data some records")
  print (" 7. Print all employee records ordered by salary")
  print (" 8. Print all employee records as text file")
  print (" 9. Load test data")
  print (" 10. Exit\n")
  __choose_menu = input("Enter your choice: ")
  db_ops = DBOperations()
  if __choose_menu == '1':
    db_ops.create_table()
  elif __choose_menu == '2':
    db_ops.insert_data()
  elif __choose_menu == '3':
    db_ops.select_all()
  elif __choose_menu == '4':
    db_ops.search_data()
  elif __choose_menu == '5':
    db_ops.update_data()
  elif __choose_menu == '6':
    db_ops.delete_data()
  elif __choose_menu == '7':
    db_ops.print_report()
  elif __choose_menu == '8':
    db_ops.print_file()  
  elif __choose_menu == '9':
    db_ops.insert_test_data()  
  elif __choose_menu == '10':
    print("System exited")
    exit(0)
  else:
    print ("Invalid choice")