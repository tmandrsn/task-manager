import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%d %b %Y"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None, id = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        id: Int
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed
        self.id = id

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        id = int(tasks[6])
        self.__init__(username, title, description, due_date, assigned_date, completed, id)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No",
            str(self.id)
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: {self.id}\t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Complete? \t {self.completed}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str
        


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    (username, password) = user.split(';')
    password = password.strip()
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))



def reg_user():
    '''
    Function to register a new user
    '''
    # Request input of a new username
    new_username = input("New Username: ")
    #check username is unique
    while (new_username in username_password):
        new_username = input("Username is taken please enter a different one: ")
        # Request input of a new password
    new_password = input("New Password: ")
    if (check_username_and_password(new_username, new_password) == True):
        # Request input of password confirmation.
        confirm_password = input("Confirm Password: ")
        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            # Add to dictionary and write to file
            username_password[new_username] = new_password
            write_usernames_to_file(username_password)
            print("New user added")
        # Otherwise you present a relevant message.
        else:
            print("Passwords do no match")
        



def new_task():
    '''
    Function to create a new task
    '''
# Prompt a user for the following:
#     A username of the person whom the task is assigned to,
#     A title of a task,
#     A description of the task and
#     the due date of the task.

# Ask for username
    task_username = input("Name of person assigned to task: ")
    if task_username in username_password.keys():
        
        # Get title of task and ensure safe for storage
        while True:
            task_title = input("Title of Task: ")
            if validate_string(task_title):
                break

        # Get description of task and ensure safe for storage
        while True:
            task_description = input("Description of Task: ")
            if validate_string(task_description):
                break

            # Obtain and parse due date
        while True:
            try:
                task_due_date = input("Due date of task (dd Mon YYY): ")
                due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                    print("Invalid datetime format. Please use the format specified")

        # Obtain and parse current date
        curr_date = date.today()

        # Get number of tasks and increase task id by 1
        task_id = len(task_list) + 1


        # Create a new Task object and append to list of tasks
        new_task = Task(task_username, task_title,
        task_description, due_date_time, curr_date, False, task_id)
        task_list.append(new_task)

        # Write to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
        print("Task successfully added.")
    else:
        print("User does not exist. Please enter a valid username")
        pass

def view_all():
    '''
    Display all tasks
    '''
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")

def view_mine():
    '''
    Display all tasks for user
    '''
    print("-----------------------------------")
    has_task = False
    task_num = 0
    for t in task_list:
        if t.username == curr_user: # check all tasks to see if they match user
            has_task = True
            print(t.display())
            print("-----------------------------------")

    # Let user select a task to mark complete or edit
    user_select = int(input('Select a task number to mark complete, edit or enter -1 to exit '))
    if (user_select == -1):
        print('Returning to menu')
    
    elif (user_select >= 0): # make sure is a valid positive int
        for t in task_list:
            if t.id == user_select:
                mark_edit = input('''Select one of the options below:
                m - mark task as complete
                e - edit the task
                x - exit
                 ''')
                if (mark_edit == 'm'):
                    t.completed = 'Yes'
                
                if (mark_edit == 'e'):
                    if (t.completed == False): #if task not complete
                        #edit the user assigned and due date
                        t.username = input('Enter name of new user to'
                        ' assign task to ')
                        due_date = input("Due date of task (dd Mon YYY): ")
                        date_wrong = True
                        
                        while (date_wrong == True):    
                            try: #check format is correct
                                t.due_date = datetime.strptime(due_date,
                                DATETIME_STRING_FORMAT)
                                date_wrong = False
                            except ValueError:
                                print("Invalid datetime format. Please use "
                                "the format specified ")
                                due_date = input("Due date of task (dd Mon YYY): ")
                        
                        # Write changes to task.txt
                        with open("tasks.txt", "w") as task_file:
                            task_file.write("\n".join([t.to_string() for t in task_list]))
                            print("Task successfully updated.")
                            
                    else:
                        print('Task is completed cannot be edited')

                if (mark_edit == 'x'):
                    print("-----------------------------------")

    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")

def generate_reports():
    '''
    Generate task_overview.txt and user_overview.txt
    '''
    total_task = len(task_list)
    total_completed = 0
    total_uncompleted = 0
    total_overdue = 0
    spacing = "-----------------------------------"

    #create task_overview.txt to write report
    with open ('task_overview.txt', 'w') as t:

        for task in task_list:
            if (task.completed == 'Yes'):# get completed tasks
                total_completed += 1
            else:
                total_uncompleted +=1
                if (task.due_date < datetime.now()):# get overdue tasks
                    total_overdue +=1

        #write the report
        t.write(f'{spacing}\nTotal Number of Tasks:\t\t{total_task}\n'
        f'Total Completed Tasks:\t\t{total_completed}\n'
        f'Total Uncompleted Tasks:\t{total_uncompleted}\n'
        f'Total Overdue Tasks:\t\t{total_overdue}\n'
        f'Percentage Incomplete:\t\t{round(((total_uncompleted/total_task)*100),2)}\n'
        f'Percentage Overdue:\t\t\t{round(((total_overdue/total_task)*100),2)}\n'
        f'{spacing}'
        )
    # create user_overview.txt to write report
    with open ('user_overview.txt', 'w') as u:
        for user in username_password:
            # For each user create a report
            user_task = 0
            user_completed = 0
            user_uncompleted = 0
            user_overdue = 0
            for task in task_list:
                if (task.username == user): # check tasks belong to user
                    user_task += 1
                    if (task.completed == 'Yes'):# get completed tasks
                        user_completed += 1
                    else:
                        user_uncompleted +=1
                        if (task.due_date < datetime.now()):# get overdue tasks
                            user_overdue +=1

            if (user_task == 0): # in case no tasks assigned to user
                p_uncompleted = 'na'
                p_overdue = 'na'
            else:
                p_uncompleted = round(((user_uncompleted/user_task)*100),2)
                p_overdue = round(((user_overdue/user_task)*100),2)
            

            #write the report
            u.write(f'{spacing}\n{user}\nTotal Number of Tasks:\t\t{user_task}\n'
            f'Total Completed Tasks:\t\t{user_completed}\n'
            f'Total Uncompleted Tasks:\t{user_uncompleted}\n'
            f'Total Overdue Tasks:\t\t{user_overdue}\n'
            f'Percentage Incomplete:\t\t{p_uncompleted}\n'
            f'Percentage Overdue:\t\t\t{p_overdue}\n'
            f'{spacing}\n'
            )

def display_stats():
    '''
    Display statistics for tasks and users
    '''
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")
    #generate reports if they dont exist
    if not(os.path.exists('task_overview.txt') and os.path.exists('user_overview.txt')):
        generate_reports() 
    print('Task Statistics\n')
    #open task_overview.txt and print contents    
    with open('task_overview.txt','r',encoding='utf-8') as t:
        for line in t:
            print(f'{line} ')
    print("-----------------------------------")
    #open user_overview.txt and print contents    
    print('User statistics \n')
    with open('user_overview.txt','r',encoding='utf-8') as u:
        for line in u:
            print(line)
    print("-----------------------------------")
            


#########################
# Main Program
######################### 

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()


    if menu == 'r': # Register new user (if admin)
        # Request input of a new username
        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            continue
        reg_user()


    elif menu == 'a': # Add a new task
        new_task()

    elif menu == 'va': # View all tasks
        view_all()

    elif menu == 'vm': # View my tasks
        view_mine()

    elif menu == 'gr': # Generate reports
        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            continue
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin': 
        # If admin, display statistics
        display_stats()

    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again")