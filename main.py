

username = input("Enter username : ").lower()
user_exist = False
with open("users.txt" , "r") as user_file :

    for logged_users in user_file: # file daki satırları tek tek okur
        logged_users = logged_users.strip() # başındaki ve sondaki boşlukları ve \n i siler
        if (logged_users == username) :
            print(f"Welcome back {username} !")
            user_exist = True
            break

with open("users.txt" , "a") as user_file :
    if not user_exist :
        print("User creating ...")
        user_file.write(f"{username}\n")
        print(f"Welcome {username}!")


#adding tasks func


task_file = f"{username}_tasks.txt"

def task_writer(task_file): 

    with open(task_file , "a") as user_task_file :

        while (True) :
            task = input("Enter new task (to exit press 1) : ")

            if task == "1" :
                break

            if len(task) > 100:
                print("Görev çok uzun, tekrar dene.")
                continue
        
            user_task_file.write(f"{task} \n") 
    print("Tasks saved !")

#task read func

def task_reader(task_file):

    try:
        with open(task_file , "r") as user_task_file :
            lines = user_task_file.readlines()

            if not lines :
                print("Task list is empty")

            else:
                for i , line in enumerate(lines , start = 1 ):
                    print(f"{i}- {line.strip()}")


    except FileNotFoundError:
        
        print("File cannot be found new file creating...")
        
        with open(task_file , "x") as user_task_file :

            pass

def delete_task(task_file): 
    print("Tasks: ")
    try:
        with open(task_file , "r") as user_task_file :
            lines = user_task_file.readlines()

            if not lines :
                print("Task list is empty")
                return

            for i , line in enumerate(lines , start = 1 ):
                print(f"{i}- {line.strip()}")


        max_input = len(lines)
        while True :
            delete_input_list = input("Please choose the tasks that you want to delete (put comma between numbers) : ").split(",")

            if delete_input_list == ['']:
                print("No input provided.")
                return
            try:
                delete_indexes = [int(i.strip()) for i in delete_input_list]
            except ValueError:
                print("Please enter valid numbers separated by commas.")
                continue

            for i in delete_indexes:
                if i < 1 or i > max_input :
                    print("invalid input , try again!")
                    break

            else:

                new_task = []
                for i , task in enumerate(lines , start= 1) :
                    if i not in delete_indexes:
                        new_task.append(task)

                with open(task_file , "w") as user_task_file :

                    for task in new_task :
                        user_task_file.write(task)
                print("Deleting completed!")

                print("\nUpdated task list:")
                task_reader(task_file)
                break
            continue


    except FileNotFoundError:
        print("File cannot be found. Firstly create a file. (to create a file choose option 2 - add new tasks)")
        return
    except ValueError:
        print("İnvalid input")
        return



#menu
print(f"What would you like to do today {username} ?")
print(" --- ")
while (True) :

    print("1 - Read tasks")
    print("2 - Add new tasks")
    print("3 - Delete tasks")
    print("4 - Exit")
    print()
    user_choice = input(
    "Select an option :")

    match user_choice :
        case "1" :
            print(" --- ")
            task_reader(task_file)
            print(" --- ")
        case "2" :
            print(" --- ")
            task_writer(task_file)
            print(" --- ")                  
        case "3" :
            print(" --- ")
            delete_task(task_file)
            print(" --- ")
        case "4" :
            print(f"Have a nice day {username}!")
            break

        case _ :
            print("İnvalid input . Please try again!")
            print(" --- ")

    print("Anything you would like to do?")

