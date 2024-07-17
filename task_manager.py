"""Reference and research:
used for the looping through the dictionary
https://realpython.com/iterate-through-dictionary-python/
Try Catch blocks
+https://www.w3schools.com/python/python_try_except.asp
"""
import os
import pwinput 
from datetime import date
from datetime import datetime

file_path_user = 'user.txt'
file_path_tasks = 'tasks.txt'

file_path_task_overview = 'task_overview.txt'
file_path_user_overview = 'user_overview.txt'


file_validation = True
line_count = 0
error_count = 0
username_password = {}
generate_dictionary_valid = True


def update_path_dir(file_path):
    '''Update the file path to include the current directory of the script file.'''

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the text file
    text_file_path = os.path.join(current_directory, file_path)
    return text_file_path 

file_path_user = update_path_dir(file_path_user)
file_path_tasks = update_path_dir(file_path_tasks)
task_report_path = update_path_dir(file_path_task_overview)
user_report_path = update_path_dir(file_path_user_overview)

def file_validation(file_path,error_msg='File could not be found!'):
    ''' - Checking if a file is valid. 
     - Allows the user to specify an error msg to display.
    '''
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the text file
    text_file_path = os.path.join(current_directory, file_path)

    is_valid = True
    if os.path.exists(text_file_path) != True:
        print(error_msg)
        is_valid = False
    return is_valid

def generate_username_password_dict(file_path_user):
    '''- Checks if the user.txt file has data.
     - Checks that there is a username and password found on each line
      if not an error message will be printed with the line number.
     - Adds username and password to dictionary if the line is valid.
     - if line_count == error_count then that means that none of the data
     in the user.txt file is in the correct format false will be returned.
    '''
    line_count = 0
    error_count =0
    user_file_valid = True
    with open(file_path_user,'r' ) as file:
        for line in file: 
            # The lines are counted to keep track of where an error may be.
            line_count +=1
            if len(line) == 0:
                print('ERROR! user.txt file has not data!')
            else:
                line_split = line.strip().split(',')
                if len(line_split) >= 2:
                    username_password[line_split[0].strip()] = line_split[1].strip()
                elif len(line_split) <= 1:
                    error_count +=1
                    print(f'Error on line {str(line_count)} in file users.txt. Expected data format : username,password')
        if line_count == error_count:
            print(f'ERROR! {file_path_user} file invalid format please check. Expected data format : username,password')
            user_file_valid = False
    return user_file_valid

def input_validation(input_string, is_password):
    ''' - Validates if the user has input anything.
     - It also will mask the user input if is_password is set to true.
    '''
    user_input = ''
    while len(user_input) == 0:
        if is_password:
            user_input = pwinput.pwinput(prompt=f'{input_string}') 
        else:
            user_input = input(input_string)
        # Checking if the user has input anything
        if len(user_input) == 0:
            print('You have not entered anything!')
    return user_input


user_file_error_msg = f'ERROR! {file_path_user} is a required file and could not be found! \nThe program will now exit.'
if file_validation(file_path_user,user_file_error_msg) != True:
    exit()
else:
    generate_dictionary_valid = generate_username_password_dict(file_path_user)
    if generate_dictionary_valid == False:
        exit()

#ask the user to input login details
password_valid = False
username_input = ''
while len(username_input) == 0:
    username_input = input_validation('Please enter your username:\n',False)
    if len(username_input) >0:
        #check if username is in the dictionary
        if username_input in username_password:
            # If the password is not valid the user will be continously asked to input a password
            while password_valid == False:
                password_input = input_validation('Please enter password:\n',True)
                if len(password_input) >0:
                    if username_password.get(username_input) == password_input:
                        print(f'Welcome {username_input}')
                        password_valid = True
                    else:
                        print('Sorry you have entered the incorrect password entered!')
        else:
            print('The username you have enetered could not be found.\n')
            username_input = ''
   

def reg_user():
    ''' - The username entered by will be check if it already exists.
     - If it does exist the user will be asked to try a another username.
     else if it does not exist the user will be asked to input the password.
     - The password will need to be entered twice to confirm this is the password to register.
     - The username and password will then be written to the user.txt file
     - The generate_username_password_dict is called again to update the username_password dictionary
     for future use in the program such as adding task for newly created user.
    
    '''
    username_already_exist = True
    while username_already_exist == True:
        reg_username = input_validation('Please enter the username you would like to register:\n',False)
        if reg_username in username_password:
            print('This username already exists!')
        else:
            username_already_exist = False
    reg_password = input_validation('Please enter the password you would like to register:\n',True)
    password_match = False
    while password_match == False:
        confirmation_password = input_validation('Please confirm your password by entering it again:\n ',True)
        if(reg_password != confirmation_password):
            print('The password you have entered does not match please try again.')
        else:
            password_match = True
    with open(file_path_user,'a+' ) as file:
            file.writelines(f'{reg_username}, {reg_password}\n')
    generate_username_password_dict('user.txt')
    
def add_task():
    ''' - Checking the username is valid that the user would like to assign the task too
     - Asking the user for the title, description(this value can be null) and
     due_date which is validated for correct data type.
     - assigned date is set to today's date and completed is set to no.
     - The details are written to the task.txt file    
    '''
    username_isValid = False
    while username_isValid == False:
        add_username = input_validation('What is the username of whom you would like to assign the task:\n',False)
        if add_username in username_password:
            username_isValid = True
        else:
            print('You have not entered a valid username. Please try again.')

    add_task_title = input_validation('What is the title of the task:\n',False)
    add_task_description = input('What is the description of the task: \n')
    add_assign_date = date.today().strftime('%d %b %Y')
    converted_due_date = date.today().strftime('%d %b %Y')
    add_task_completed = 'No'

    date_validation = False
    while date_validation == False:
        add_task_date = input_validation('What is the due date of the task:(eg. 12 Feb 2024) \n',False)
        # Converting and formatting add_task_date that the user has input
        # catching any convertion errors and asking the user to input a date until convertion is valid
        try:
            converted_due_date = datetime.strptime(add_task_date, '%d %b %Y')
            date_validation = True
        except:
            print('An error occured when trying to convert the date to the required format.Please try again.')
            date_validation = False
    with open(file_path_tasks,'a+' ) as file:
            file.writelines(f'{add_username},{add_task_title},{add_task_description},{add_assign_date},{datetime.strftime(converted_due_date, '%d %b %Y')},{add_task_completed}\n')
    print('Add task successful!')

def generate_task_dictionary():
    ''' - Stores all the valid tasks to a dictionary
    '''
    task_dictionary = {}
    count_line = 0 #used for the key of the dictionary
    with open(file_path_tasks,'r') as file:
        for lines in file:
            count_line +=1
            line  = lines.strip().split(',')
            if len(line) > 1:
                task_dictionary[count_line] = line
    return task_dictionary

def print_task_line(task_id, task_details):
    ''' Prints the task ID supplied and task details
    '''
    print(f'''__________________________________________________________________________________\n
Task ID:                {task_id}
Task:                   {task_details[1]}
Assigned to:            {task_details[0]}
Date Assigned:          {task_details[3]}
Due date:               {task_details[4]}
Task complete?          {task_details[5]}
Task description:
{task_details[2]}
''')
    
def view_all():
    ''' Displaying all the task
    '''
    task_dictionary = generate_task_dictionary()
    for task_id, task_details in task_dictionary.items():
        print_task_line(task_id,task_details)
   
def view_mine(username):
    ''' - Displaying all task for the currently logged in user.
     - Allowing the user to edit any of their tasks as long as it's not marked as completed.
    '''
    task_dictionary = generate_task_dictionary()
    for task_id, task_details in task_dictionary.items():
        if task_details[0] == username:
            print_task_line(task_id,task_details)
    valid_input = False
    while valid_input == False:
        edit_input = input_validation('To edit a task enter the task ID -1 to return to the main menu:\n',False)
        # if the user does not input an int an error is thrown.
        try:
            int(edit_input)
            if edit_input == '-1':
                print('Returning to the main menu now.')
                valid_input = True
            else:
                #checking if the task ID input is a valid task id and is associated with the current user
                if int(edit_input) not in task_dictionary:
                    print('You have not input a valid task ID please try again.')
                    valid_input = False
                elif  int(edit_input) in task_dictionary and task_dictionary[int(edit_input)][0] != username:
                    print('You have not input a valid task ID please try again.')
                    valid_input = False
                elif  int(edit_input) in task_dictionary and task_dictionary[int(edit_input)][0] == username and (task_dictionary[int(edit_input)][5]).lower() == 'yes':
                    print('You cannot edit a task marked as completed.')
                    valid_input = False
                else:
                    valid_input = True
                    # Validating user input for update question is a y/n
                    # While validate_quest_1 is false continuously ask the user for input
                    # else set to True if they have input the right choice
                    validate_quest_1 = False
                    while validate_quest_1 == False:
                        mark_completed = input_validation('Would you like to mark the task as completed?(y/n):\n',False)
                        if mark_completed.lower() == 'y':
                            task_dictionary[int(edit_input)][5] = 'yes'
                            validate_quest_1 = True
                        elif mark_completed.lower() == 'n':
                            validate_quest_1 = True
                        elif mark_completed.lower() != 'y'or mark_completed.lower() != 'n':
                            validate_quest_1 = False
                            print('You have not entered a valid option please try again.')
                    validate_quest_2 = False
                    while validate_quest_2 == False:
                        due_date_edit = input_validation('Would you like to edit the due date of the task?(y/n):\n',False)
                        if due_date_edit.lower() == 'y':
                            validate_quest_2 = True
                            converted_due_date = date.today().strftime('%d %b %Y')
                            date_validation = False
                            while date_validation == False:
                                due_date_value = input_validation('What is the new due date of the task:(eg. 12 Feb 2024) \n',False)
                                # Converting and formatting add_task_date that the user has input
                                # catching any convertion errors and asking the user to input a date until convertion is valid
                                try:
                                    converted_due_date = datetime.strptime(due_date_value, '%d %b %Y')
                                    task_dictionary[int(edit_input)][4] = datetime.strftime(converted_due_date, '%d %b %Y')
                                    date_validation = True
                                except:
                                    print('An error occured when trying to convert the date to the required format.Please try again.')
                                    date_validation = False
                        elif due_date_edit.lower() == 'n':
                            validate_quest_2 = True
                        elif due_date_edit.lower() != 'y'or due_date_edit.lower() != 'n':
                            validate_quest_2 = False
                            print('You have not entered a valid option please try again.')
                    validate_quest_3 = False
                    while validate_quest_3 == False:
                        assigned_username_edit = input_validation('Would you like to change who the task is assigned to?(y/n)\n',False)
                        if assigned_username_edit.lower() == 'y':
                            validate_quest_3 = True
                            username_valid = False
                            while username_valid == False:
                                username_edit = input_validation('What is the username of To whom would you like to re-assign the task:\n',False)
                                #checking if the username is valid
                                if username_edit in username_password:
                                    username_valid = True
                                    task_dictionary[int(edit_input)][0] = username_edit
                                else:
                                    username_valid = False
                                    print('You have not entered a valid username.')
                        elif assigned_username_edit.lower() == 'n':
                            validate_quest_3 = True
                        elif assigned_username_edit.lower() != 'y'or assigned_username_edit.lower() != 'n':
                            validate_quest_3 = False
                            print('You have not entered a valid option please try again.')
        except:
            print('You have not entered a valid option please try again!')
            valid_input = False
            
    #write the updated task dictionary to the task file
    with open(file_path_tasks,'w+' ) as file:
        for line in task_dictionary:
            file.writelines(f'{task_dictionary[line][0]},{task_dictionary[line][1]},{task_dictionary[line][2]},{task_dictionary[line][3]},{task_dictionary[line][4]},{task_dictionary[line][5]}\n')
    print('Edit task successful!')

def generate_report_task():
    '''Generates the task_overview.txt report
    '''
    task_dictionary = generate_task_dictionary()
    task_total = len(task_dictionary)
    completed_task_total = 0
    incompleted_task_total = 0
    overdue_incomplete_tasks = 0
    percentage_task_incomplete = 0
    percentage_task_overdue = 0
    compare_date = datetime.today()
    
    for key,value in task_dictionary.items():
        if value[5].lower() == 'yes':
            completed_task_total +=1
        elif value[5].lower() == 'no':
            incompleted_task_total +=1

            converted_date  = datetime.strptime(value[4].strip(), '%d %b %Y')
            if  compare_date > converted_date:
                overdue_incomplete_tasks +=1
    percentage_task_incomplete = (incompleted_task_total / task_total) * 100
    percentage_task_overdue = (overdue_incomplete_tasks/task_total) * 100

    

    with open(task_report_path,'w+') as file:
        file.writelines(f'--> TASK OVERVIEW REPORT <--\n')
        file.writelines(f'The total number of tasks that have genereated and tracked are :      {task_total}\n')
        file.writelines(f'The total number of tasks that are completed :                        {completed_task_total}\n')
        file.writelines(f'The total number of incomplete task :                                 {incompleted_task_total}\n')
        file.writelines(f'The total number of incomplete task that are overdue :                {overdue_incomplete_tasks}\n')
        file.writelines(f'The percentage of tasks that are incomplete :                         {percentage_task_incomplete}\n')
        file.writelines(f'The percentage of tasks that are overdue :                            {percentage_task_overdue}\n')

def generate_task_list(username):
    ''' Create a task_list for a specific user.
    '''
    task_list = []
    with open(file_path_tasks,'r') as file:
        for line in file:
            line_split = line.strip().split(',')
            if line_split[0] == username:
                task_list.append(line_split)  
    return task_list

def generate_report_user():
    ''' Generates the user_overview.txt report.
     - stats based on all the registered users.
    '''  
    task_dictionary = generate_task_dictionary()
    task_total = len(task_dictionary)
    total_reg_user = len(username_password)
    
    
    with open(user_report_path,'w+') as file:
        file.writelines('--> THE USERS OVERVIEW REPORTS <--\n')
        file.writelines(f'The total number of users registered :                                   {total_reg_user}\n')
        file.writelines(f'The total number of tasks that have genereated and tracked are :         {task_total}\n\n')
        for key_username in username_password.keys():
            task_list = generate_task_list(key_username)
            percentage_user_tasks = 0
            total_user_task_copmleted = 0
            total_user_task_incopmleted = 0
            total_task_incopmleted_overdue = 0
            compare_date = datetime.today()
            total_user_tasks = len(task_list)
            # user specific stats calulated only if there are tasks assigned to the user
            if total_user_tasks > 0:
                for task  in task_list:
                    percentage_user_tasks = (total_user_tasks / task_total) * 100
                    if task[5].lower() == 'yes':
                        total_user_task_copmleted +=1
                    elif task[5].lower() == 'no':
                        total_user_task_incopmleted +=1
                        converted_date  = datetime.strptime(task[4].strip(), '%d %b %Y')
                        if compare_date > converted_date:
                                total_task_incopmleted_overdue +=1

            file.writelines(f'--User overview report for {key_username}--\n')
            file.writelines(f'The total number of tasks assigned to the user :                         {total_user_tasks}\n')
            file.writelines(f'The percentage of tasks assigend :                                       {percentage_user_tasks}\n')
            file.writelines(f'The percentage of tasks assigend that are completed :                    {total_user_task_copmleted}\n')
            file.writelines(f'The percentage of tasks assigend that are incompleted :                  {total_user_task_incopmleted}\n')
            file.writelines(f'The percentage of tasks assigend that are incomplete and overdue :       {total_task_incopmleted_overdue}\n\n')
        
def print_reports():
    ''' Prints the task_overview.txt and user_overview.txt.
     - if no files found an error message will be displayed.
    '''
    try:
        with open(file_path_task_overview,'r') as file:
            for line in file:
                print(line.strip()) 
        print('')
    except FileNotFoundError:
        print('No task overview data to display please try generating the report.\n')
    try:
        with open(file_path_user_overview,'r') as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print('No user overview data to display please try generating the report.\n')
            
while password_valid:
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.
    if username_input =='admin':
        menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit
: ''').lower()
    else:
        menu = input('''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').lower()

    if menu == 'r':
        reg_user()  
    elif menu == 'a':
        add_task()    
    elif menu == 'va':
        view_all()  
    elif menu == 'vm':
        view_mine(username_input)  
    elif menu == 'gr':
        generate_report_task()
        generate_report_user()
    elif menu == 'ds':
        print_reports()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have entered an invalid input. Please try again")