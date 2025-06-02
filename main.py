

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


#adding tasks


task_file = f"{username}_tasks.txt"

with open(task_file , "a") as user_task_file :

    while (True) :
        task = input("Enter new task (to exit press 1) : ")

        if task == "1" :
            break
        if len(task) > 100:
            print("Görev çok uzun, tekrar dene.")
            continue
        
        user_task_file.write(f"{task} \n") 
        task = input("Enter new task (to exit press 1) : ")
print("Tasks saved !")

