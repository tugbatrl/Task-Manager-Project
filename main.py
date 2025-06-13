import json
import os

username = input("Enter username : ").lower()
user_exist = False
with open("user.txt" , "r") as user_file :

    for logged_users in user_file: # file daki satırları tek tek okur
        logged_users = logged_users.strip() # başındaki ve sondaki boşlukları ve \n i siler
        if (logged_users == username) :
            print(f"Welcome back {username} !")
            user_exist = True
            break

with open("user.txt" , "a") as user_file : #eğer kullanıcı yoksa yeni bir kullanıcı oluşturur
    if not user_exist :
        print("User creating ...")
        user_file.write(f"{username}\n")
        print(f"Welcome {username}!")

task_file = f"{username}_tasks.json"

def json_file_check(task_file) : #json dosyasındaki görevleri listeye dönderen helper fonksiyon

    if os.path.exists(task_file) :
            try:
                with open(task_file , "r") as user_task_file:
                    return json.load(user_task_file)
            except json.JSONDecodeError :
                return []
    else :
        print("Task file cannot be found. New file creating...") #dosya yoksa yeni dosya oluşturur
        with open(task_file ,"w") as user_task_file:
            json.dump([],user_task_file)
            return []
        print("Completed!")


def task_writer(task_file):  #Görev yazma fonksiyonu

    task_list = json_file_check(task_file)

    while (True) :
        task = input("Enter new task (to exit press 1) : ")

        if task == "":
            print("Task cannot be empty! Try again.")
            continue

        if task == "1" :
            break

        if len(task) > 100:
            print("Task is too long, try again.")
            continue

        category = input("Enter category (to skip press enter): ")
        due_date = input("Enter due date (to skip press enter): ")
        
        task_dic = {
            "task" : task ,
            "category" : category if category else None,
            "due_date" : due_date if due_date else None,
            "completed": False
            }

        task_list.append(task_dic)

    with open(task_file , "w") as user_task_file : #Görevleri json dosyasına yazar
        json.dump(task_list ,user_task_file, indent=4)
    print("Tasks saved !")

def task_reader(task_file): #Görev okuma fonksiyonu

    task_list = json_file_check(task_file)

    if not task_list :
        print("Task list is empty")

    else:
        for i , task in enumerate(task_list , start = 1 ): #Tamamlanmış görevleri işaretleyerek yazdırır
            if task["completed"] == False :
                print(f"[ ] {i}- Task : {task['task']}\n - Category : {task['category']}\n - Due date : {task['due_date']}")
                print()
            elif task["completed"] == True :
                print(f"[x] {i}- Task : {task['task']}\n - Category : {task['category']}\n - Due date : {task['due_date']}")
                print()



def delete_task(task_file):  #Görev silme fonksiyonu

    try:
        task_list = json_file_check(task_file)
        print("Tasks:")
        task_reader(task_file)
        if not task_list:
            return

        while True :  #Çoklu silme için birden fazla görev alır
            delete_input_list = input("Please choose the tasks that you want to delete (put comma between numbers) : ").split(",")
            #Hatalı input kontrolü
            if delete_input_list == ['']:
                print("No input provided.")
                return
            try:
                delete_indexes = [int(i.strip()) for i in delete_input_list]
            except ValueError:
                print("Please enter valid numbers separated by commas.")
                continue

            for i in delete_indexes:
                if i < 1 or i > len(task_list) :
                    print(f"Please enter between 1 and {len(task_list)} ")
                    break

            else:

                new_task = []
                for i , task in enumerate(task_list , start= 1) :  #Silinmeyecek olan görevleri yeni listeye atar
                    if i not in delete_indexes:
                        new_task.append(task)

                with open(task_file , "w") as user_task_file :
                    json.dump(new_task , user_task_file , indent=4) #Json dosyasını yeniden yazdırır

                print("Deleting completed!")
                print("\nUpdated task list:")
                task_reader(task_file)
                break
            continue

    except ValueError:
        print("İnvalid input")
        return

def edit_task(task_file): #Görev editleme fonksiyonu

    task_list = json_file_check(task_file)
    print("Tasks:")
    task_reader(task_file)
    if not task_list:
        return
    #Tek seferde 1 görev düzenler

    while True :
        try:
            user_choice = int(input("Choose the task to edit :"))

            if user_choice < 1 or user_choice > len(task_list) :
                print(f"Please enter between 1 and {len(task_list)} ")
                continue

            else:

                while True:

                    new_task = input("Enter new task: ")
                    if new_task == "":
                        print("Task cannot be empty! Try again.")
                        continue
                    break
        except ValueError:
            print("Please enter only 1 number")
            continue

        new_category = input("Enter category (to skip press enter): ") #Tüm görevleri baştan editler
        new_due_date = input("Enter due date (to skip press enter): ")

        task_list[user_choice - 1]["task"] = new_task
        task_list[user_choice - 1]["category"] = new_category if new_category else None
        task_list[user_choice - 1]["due_date"] = new_due_date if new_due_date else None

        with open(task_file , "w") as user_task_file :
            json.dump(task_list , user_task_file , indent= 4)

        break

    print("Task edited succesfully!")
    print("\n")
    print("New task list : ")
    task_reader(task_file)


def mark_task(task_file) : #Tamamlanan görevleri işaretleme fonksiyonu

    task_list = json_file_check(task_file)
    print("Tasks :")
    task_reader(task_file)
    if not task_list:
        return

    while True:
        try:
            #hatalı input kontrolü
            user_choice = int(input("Which task would you like to mark as completed?: "))
        except ValueError:
            print("Please enter a number")
            continue

        if user_choice < 1 or user_choice > len(task_list) :
            print(f"Please enter between 1 and {len(task_list)} ")
            continue
        break

    if task_list[user_choice -1]["completed"]: #Görev zaten tamamlanmışsa uyarı verir
        print("This task is already marked as completed.")
        return

    task_list[user_choice -1]["completed"] = True 

    with open(task_file , "w") as user_task_file:
        json.dump(task_list , user_task_file , indent=4)
    print()
    print(f"Task '{task_list[user_choice -1]['task']}' marked as completed! ✅")

def filter_task(task_file) : #Görev filtreleme fonksiyonu
    #Görevleri tamamlanmış ya da tamamlanmamış olarak filtreleyip gösterir

    task_list = json_file_check(task_file)
    if not task_list:
        print("Task list is empty!")
        return

    while True:
        try:
            print()
            print("1- Show completed")
            print("2- Show incompleted")

            user_choice = int(input("Choose Filter: "))

            if user_choice < 1 or user_choice > 2 :
                print(f"Please enter between 1 and 2 ")
                continue
            break
        except ValueError:
            print("Please enter a number")
            continue

    if user_choice == 1:
        completed_tasks = [task for task in task_list if task["completed"]] #Tamamlanmış görev yoksa uyarı verir
        if not completed_tasks:
            print("There are no completed task")
            return

        for i , task in enumerate(task_list , start = 1 ):#Sadece tamamlanmış görevleri yazdırır
            if task["completed"] == True:
                print()
                print(f"[x] {i}- Task : {task['task']}\n - Category : {task['category']}\n - Due date : {task['due_date']}")
                print()

    elif user_choice == 2:
        incompleted_tasks = [task for task in task_list if not task["completed"]] #Tamamlanmamış görev yoksa uyarı verir
        if not incompleted_tasks:
            print("There are no incompleted task")
            return

        for i , task in enumerate(task_list , start = 1 ): #Sadece tamamlanmış görevleri yazdırır
            if task["completed"] == False :
                print()
                print(f"[ ] {i}- Task : {task['task']}\n - Category : {task['category']}\n - Due date : {task['due_date']}")
                print()


def delete_completed_tasks(task_file): #Tamamlanmış tüm görevleri silen fonksiyon

    task_list = json_file_check(task_file)
    print("Tasks :")
    task_reader(task_file)
    if not task_list:
        return

    completed_tasks = [task for task in task_list if task["completed"]] #Tamamlanmış görev yoksa hata verir
    if not completed_tasks:
        print("There are no completed tasks")
        return

    incompleted_tasks = incompleted_tasks = [task for task in task_list if not task["completed"]]

    with open(task_file , "w") as user_task_file :
        json.dump(incompleted_tasks , user_task_file , indent=4)

    print("Completed tasks deleted!")
    print("\nUpdated task list:")
    task_reader(task_file)


#menü

print(f"What would you like to do today {username} ?")
print(" --- ")
while (True) :
#Kullanıcıya seçenekleri gösterir
    print("1 - Read tasks")
    print("2 - Add new tasks")
    print("3 - Delete tasks")
    print("4 - Edit tasks")
    print("5 - Mark completed tasks") 
    print("6 - Exit")
    print()
    user_choice = input(
    "Select an option :")

    match user_choice : #match-case ile kullanıcı seçimini yönetir
        case "1" :
            print(" --- ")
            print("1- Show all task")
            print("2- Use filter")
            while True:
                try:
                    user_r_choice = int(input("Choose 1 or 2: "))
                    if user_r_choice < 1 or user_r_choice > 2 :
                        print(f"Please enter 1 or 2 ")
                        continue
                    break
                except ValueError:
                    print("Please enter a number")
                    continue
            if user_r_choice == 1:
                print()
                task_reader(task_file)
            elif user_r_choice == 2:
                filter_task(task_file)
            print(" --- ")
        case "2" :
            print(" --- ")
            task_writer(task_file)
            print(" --- ")                  
        case "3" :
            print(" --- ")
            print("1- Select task to delete")
            print("2- Delete all completed tasks")

            while True:
                try:
                    user_r_choice = int(input("Choose 1 or 2: "))
                    if user_r_choice < 1 or user_r_choice > 2 :
                        print(f"Please enter 1 or 2 ")
                        continue
                    break
                except ValueError:
                    print("Please enter a number")
                    continue
            if user_r_choice == 1:
                delete_task(task_file)
            elif user_r_choice == 2:
                delete_completed_tasks(task_file)
            print(" --- ")
        case "4" :
            print(" --- ")
            edit_task(task_file)
            print(" --- ")
        case "5" :
            print(" --- ")
            mark_task(task_file)
            print(" --- ")
        case "6" :
            print(f"Have a nice day {username}!")
            break

        case _ :
            print("İnvalid input . Please try again!")
            print(" --- ")

    print("Anything you would like to do?")

