# ---------------------------------------------------------------------------- #
# Title: Assignment 06
# Description: Working with functions in a class,
#              When the program starts, load each "row" of data
#              in "ToDoToDoList.txt" into a python Dictionary
#              Add the each dictionary "row" to a python list "table"
# ChangeLog (Who,When,What):
# RRoot,1.1.2030,Created started script
# RRoot,1.1.2030,Added code to complete assignment 5
# KPollock, 11.19.2021, Modified code to complete assignment 6
# ---------------------------------------------------------------------------- #

# Data ---------------------------------------------------------------------- #
# Declare variables and constants
strFileName = "ToDoFile.txt"  # The name of the data file
objFile = None  # An object that represents a file
lstTable = []  # A list that acts as a 'table' of rows
strChoice = ""  # Captures the user option selection
strTask = ""  # Captures the user task data
strPriority = ""  # Captures the user priority data
unsaved_changes = False

# Processing  --------------------------------------------------------------- #
class Processor:
    """  Performs Processing tasks """

    @staticmethod
    def read_data_from_file(file_name):
        """ Reads data from a file into a list of dictionary rows
        :param file_name: (string) with name of file
        :return: (list) of dictionary rows
        """
        list_of_rows = []  # start with empty list
        file = open(file_name, "r")
        for line in file:
            task, priority = line.split(",")
            Processor.add_data_to_list(task, priority, list_of_rows)
        file.close()
        return list_of_rows

    @staticmethod
    def add_data_to_list(task, priority, list_of_rows):
        """ Adds data (task and priority) to list
        :param task: (string) with name of task performed
        :param priority: (string) high, med, low for task
        :param list_of_rows: (list) of dictionary rows with task (key) and priority (value)
        :return: (list) updated list of rows
        """
        list_of_rows.append({"Task": task.strip(), "Priority": priority.strip()})
        return list_of_rows

    @staticmethod
    def remove_data_from_list(task, list_of_rows):
        """ Removes data from the list (task and priority)
        :param task: (string) with name of task to be removed
        :param list_of_rows: (list) of dictionary rows with task (key) and priority (value)
        :return: (list) updated list of rows
        """
        for row in list_of_rows:
            if row["Task"].lower() == task.lower():
                list_of_rows.remove(row)
        return list_of_rows

    @staticmethod
    def write_data_to_file(file_name, list_of_rows):
        """ Writes data from the list to the file using csv
        :param file_name: (string) with name of file
        :param list_of_rows: (list) you filled with file data
        :return: list of rows that was written to file
        """
        file = open(file_name, "w")
        for row in list_of_rows:
            file.write(row["Task"] + ',' + row["Priority"] + '\n')
        file.close()
        return list_of_rows


# Presentation (Input/Output)  -------------------------------------------- #
class IO:
    """ Performs Input and Output tasks """

    @staticmethod
    def print_menu_tasks():
        """  Display a menu of choices to the user

        :return: nothing
        """
        print('''
        Menu of Options
        1) Add a new Task
        2) Remove an existing Task
        3) Save Data to File        
        4) Reload Data from File
        5) Exit Program
        ''')
        print()  # Add an extra line for looks

    @staticmethod
    def input_menu_choice():
        """ Gets the menu choice from a user

        :return: string
        """
        choice = input("Which option would you like to perform? [1 to 5] - ").strip()
        print()  # Add an extra line for looks
        return choice

    @staticmethod
    def print_current_tasks_in_list(list_of_rows):
        """ Shows the current Tasks in the list of dictionaries rows

        :param list_of_rows: (list) of rows you want to display
        :return: nothing
        """
        print("******* The Current Tasks ToDo are: *******")
        for row in list_of_rows:
            print(row["Task"] + " (" + row["Priority"] + ")")
        print("*******************************************")
        print()  # Add an extra line for looks

    @staticmethod
    def input_yes_no_choice(message):
        """ Gets a yes or no choice from the user
        :param (string) message/question for yes/no answer
        :return: (Bool) 'yes' is True, 'no' is False
        """
        while True:
            answer = input(message).strip().lower()
            if answer == 'yes':
                return True
            elif answer == 'no':
                return False
            else:
                print("Please enter only 'yes' or 'no'")

    @staticmethod
    def input_new_task_and_priority():
        """ User enters a new task and priority
        :return: (tuple) of strings with task and priority
        """
        task = input('What task would you like to add? ').replace(',', '')
        priority = input('What is the priority [high, med, low]? ').replace(',', '')
        print()  # extra line for looks
        return task, priority

    @staticmethod
    def input_task_to_remove():
        """ User enters a task to remove
        :return: (string) with task to be removed
        """
        task = input("What task would you like to remove? ").strip()
        print()
        return task


# Main Body of Script  ------------------------------------------------------ #

# Step 1 - When the program starts, Load data from ToDoFile.txt.
try:
    lstTable = Processor.read_data_from_file(strFileName)
except FileNotFoundError:
    pass

while True:
    # Display a menu of choices to the user
    IO.print_menu_tasks()
    strChoice = IO.input_menu_choice()
    print()  # adding a new line for looks

    if strChoice == '1':  # Add a new task and priority
        strTask, strPriority = IO.input_new_task_and_priority()
        Processor.add_data_to_list(strTask, strPriority, lstTable)
        unsaved_changes = True
        print('Task added!')
        IO.print_current_tasks_in_list(lstTable)

    elif strChoice == '2':  # Remove a task
        IO.print_current_tasks_in_list(lstTable)
        strTask = IO.input_task_to_remove()
        Processor.remove_data_from_list(strTask, lstTable)
        unsaved_changes = True
        print('Task removed!')
        IO.print_current_tasks_in_list(lstTable)

    elif strChoice == '3':  # Save Data to File
        response = IO.input_yes_no_choice('Would you like to save your data to the file [yes or no]? ')
        if response:
            Processor.write_data_to_file(strFileName, lstTable)
            unsaved_changes = False
            print('Data saved!')
            IO.print_current_tasks_in_list(lstTable)
        else:
            print('Data has not been saved.')

    elif strChoice == '4':  # Reload Data from File
        if not (unsaved_changes and not IO.input_yes_no_choice(
                "Are you sure you want to reload data from file w/o saving [yes or no]? ")):
            lstTable = Processor.read_data_from_file(strFileName)
            print('Data reloaded')
            IO.print_current_tasks_in_list(lstTable)
        else:
            print("File data was not reloaded")

    elif strChoice == '5':  # Exit Program
        if unsaved_changes and not IO.input_yes_no_choice("Are you sure you want to exit without saving [yes or no]? "):
            print('Enter option 3 to save data.')
            continue
        print("Goodbye!")
        break

    else:
        print(strChoice, "is not an option. Please select [1 to 5].")
