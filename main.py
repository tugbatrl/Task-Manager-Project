

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



