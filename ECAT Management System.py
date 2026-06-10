# -------------------------------------------- UET-ECAT-TEST --------------------------------------------------------

# Import Libraries.
import os
import random
import json
import datetime
import time
import re
import random
import uuid

# ALL FILE EXISTS. Login, Admin, Quizz, Result.
# ----------------------------------------------------------ADMIN FILE ----------------------------------------------
def admin_file_exists():
    try:
        with open("Admin.json", "r") as file:
            admin_data = json.load(file)
            return admin_data
    
    except:
        return[]
    
admin_file_exists()

# Write Admin file.
admin_data = admin_file_exists()

with open("Admin.json", "w") as file:
    json.dump(admin_data, file, indent=4)


# ------------------------------------------------LOGIN FILE -------------------------------------------------------
def login_file_exists():
    try:
        with open("Login.json", "r") as file:
            login_data = json.load(file)
            return login_data
        
    except:
        return []
    
login_file_exists()

# write Login JSON file.
login_data = login_file_exists()

with open("Login.json", "w") as file:
    json.dump(login_data, file, indent=4)


# ------------------------------------------------------ QUIZZ FILE --------------------------------------------------
def quizz_file_exists():
    try:
        with open("Quizz.json", "r") as file:
            quizz_data = json.load(file)
            return quizz_data
        
    except:
        return[]
    
quizz_file_exists()

# Write Quizz File
quizz_data = quizz_file_exists()

with open("Quizz.json", "w") as file:
    json.dump(quizz_data, file, indent=4)


# -----------------------------------------------------RESULT FILE --------------------------------------------------
def result_file_exists():
    try:
        with open("Result.json", "r") as file:
            json.dump(result_data, file, indent=4)
            return result_data
        
    except:
        return []
        
result_file_exists()
# Write JSON FILE.
result_data = result_file_exists()

with open("Result.json", "w") as file:
    json.dump(result_data, file, indent=4)


# ----------------------------------------------------------- ADMIN SYSTEM ------------------------------------------
# -------------------------------------------------------ADMIN SYSTEM FUNCTION --------------------------------------
def Admin_Register_Login():
    # Runs Via Infinite Loop.
    while True:
        print("-" * 20, "You Are Now in Admin Section.", "-" * 20, "\n")

        # Admin Menu
        admin_menu = [
            "1. Add Quizz Section.",
            "2. Add Question in Quizz Section.",
            "3. Edit Questions in Selected Quizz Section.",
            "4. Remove Questions from Quizz Section.",
            "5. View Registered Users.",
            "6. View User Results.",
            "7. Exit"
        ]

        # Print Admin Menu.
        for menu in admin_menu:
            print(menu)

        # Select Choice By User.
        choice = input("Select option via Number: ")

        # Check User Choices.
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            print("You Are Able to access this Admin System.\n")
        
        else:
            print("You are unable to access this system.\n")
            print("Thanks for your Understanding.\n")
            continue


        # Add Quizz section.
        if choice == "1":
            print("-" * 20, "Add Quizz Section", "-" * 20, "\n")

            # Enter Section by User.
            section_name = input("Which Section you want to add: ")

            # Section Dictionary.
            section = {
                    "Section" : section_name,
                    "Questions":[]
                }
            
            # READ JSON QUIZZ FILE.
            with open("Quizz.json", "r") as file:
                quizz_data = json.load(file)
            
            # SECTION EXISTS CHECKING   
            exists = False

            for sec in quizz_data:
                if sec["Section"].lower() == section_name.lower():
                    exists = True
                    break

            if exists:
                print("Section Already Exists.\n")
                continue
            
            # append data in quizz json file
            quizz_data.append(section)

            with open("Quizz.json", "w") as file:
                json.dump(quizz_data, file, indent=4)
                
                print("-" * 20, "Section Added Successfully", "-" * 20, "\n")

            time.sleep(3)
            os.system("cls" if os.name == 'nt' else "clear")
    

        # ADD QUESTIONS IN QUIZZ SECTION.
        elif choice == "2":
            print("-" * 20, "ADD QUESTIONS IN QUIZZ SECTION", "-" * 20, "\n")

            # SECTION INPUT BY USER
            section_name = input("In which Section you add Questions: ")

            with open("Quizz.json", "r") as file:
                quizz_data = json.load(file)

            selected_section = None

            # CHECK SECTION IF EXISTS.
            for sec in quizz_data:
                if sec["Section"].lower() == section_name.lower():
                    selected_section = sec
                    break
            
            if selected_section is None:
                print("Section Not Found.\n")
                continue
            
            # ENTER QUESTIONS BY USer
            questions = int(input("How many questions you want to add: "))

            if questions <= 0:
                print("Question number must be greater than 0.\n")
                continue
            
            # ENTER QUESTIONS BY USER
            for i in range(1, questions + 1):

                print(f"\nAdding Question {i}")

                question = input("Enter Question: ")

                option_A = input("Enter Option A: ")
                option_B = input("Enter Option B: ")
                option_C = input("Enter Option C: ")
                option_D = input("Enter Option D: ")
                
                # CORRECT ANSWER
                correct_answer = input(
                "Enter Correct Option (A/B/C/D): "
                ).upper()

                selected_section["Questions"].append(
                    {
                        "Question No": len(selected_section["Questions"]) + 1,
                        "Question": question,
                        "Options": {
                        "A": option_A,
                        "B": option_B,
                        "C": option_C,
                        "D": option_D
                        },
                        "Correct Answer": correct_answer
                    }
                )

                # EDIT JSON FILE
                with open("Quizz.json", "w") as file:
                    json.dump(quizz_data, file, indent=4)
        
                print("Questions Added Successfully.\n")

    
        # Edit Questions in each Section.
        elif choice == "3":
            print("-" * 20, "Edit questions in selected section", "-" * 20, "\n")

            edit_section = input("In which section you want to edit question: ")

            with open("Quizz.json", "r") as file:
                quizz_data = json.load(file)

            section_exists = False

            for sec in quizz_data: 
                if sec['Section'].lower() == edit_section.lower():

                    for q in sec['Questions']:
                        print(f"{q['Question No']}. {q['Question']}")

                    question_no = int(input("Enter question no you want to edit: "))

                    question_found = False

                    for q in sec['Questions']:
                        if q['Question No'] == question_no:

                            question_found = True

                            print(f"Old Question: {q['Question']}")

                            q['Question'] = input("Enter New Question: ")

                            q['Options']['A'] = input("Enter New Option A: ")

                            q['Options']['B'] = input("Enter New Option B: ")

                            q['Options']['C'] = input("Enter New Option C: ")

                            q['Options']['D'] = input("Enter New Option D: ")

                            q['Correct Answer'] = input("Enter New Correct Answer: ")

                            with open("Quizz.json", "w") as file:
                                json.dump(quizz_data, file, indent=4)

                            print("Question Edit Successfully...........\n")
                            break

                    if not question_found:
                        print("Question not Found..............\n")

                    section_exists = True
                    break

            if not section_exists:
                print("Section not Found.............\n")


        # DELETE QUESTION.
        elif choice == "4":
            print("-" * 20, "Remove questions from Quizz section", "-" * 20, "\n")

            remove_section = input("In which Section you want to remove question: ")

            with open("Quizz.json", "r") as file: 
                quizz_data = json.load(file)

            section_found = False

            for sec in quizz_data: 
                if sec['Section'].lower() == remove_section.lower():

                    for q in sec['Questions']:
                        print(f"{q['Question No']}. {q['Question']}")
                    
                    remove_count = int(input("Enter questions no you want to remove: "))

                    if remove_count > len(sec['Questions']):
                        print("You enter higher number of questions.")
                        continue

                    elif remove_count <= 0:
                        print("Please enter correct value.")
                        continue

                    else:
                        for i in range(remove_count):

                            remove_question_no = int(input("Enter question no you want to remove: "))

                            remove_question = False

                            for q in sec['Questions']:
                                if q['Question No'] == remove_question_no:
                                    sec['Questions'].remove(q)
                            
                                    remove_question = True

                                    for index, q in enumerate(sec["Questions"], start=1):
                                        q["Question No"] = index

                                    with open("Quizz.json", "w") as file:
                                        json.dump(quizz_data, file, indent=4)

                                    print("Changes Saved Successfully.\n")
                                    time.sleep(2)

                                    print("Question Succesfully removed............\n")
                                    break
                            
                            if not remove_question:
                                print("Question not found...............\n")

                section_found = True
                break    

            if section_found == False:
                print("Section not Found.......\n")      


        # View REGISTERED USERS.
        elif choice == "5":
            print("-" * 20, "VIEW REGISTERED USERS", "-" * 20, "\n")

            with open("Login.json", "r") as file:
                login_data = json.load(file)

            login_found = False

            for login in login_data:
                print(f"Student ID: {login['User ID']}")
                print(f"Student Name: {login['User Name']}")
                print(f"Student Email: {login['Email']}")
                print(f"Password: {login['Password']}")

                if login["Login"]:
                    last_login = login["Login"][-1]

                    print(
                        f"Last Accessed: "
                        f"{last_login['Login Date & Time']['Login Date']} "
                        f"{last_login['Login Date & Time']['Login Time']}"
                    )
                else:
                    print("No Login History")

                login_found = True
                continue

            if login_found == False:
                print("No one can register yourself.\n")
                break

                
            
            time.sleep(3)
        

        # VIEW USER RESULTS.
        elif choice == "6": 
            print("-" * 20, "View All User Results", "-" * 20, "\n")

            with open("Result.json", "r") as file:
                result_data = json.load(file)
            
            for r in result_data:
                print(f"User Name      : {r['User Name']}")
                print(f"User Email     : {r['User Email']}")
                print(f"Total Questions: {r['User Result'][0]['Total Questions']}")
                print(f"Total Marks    : {r['User Result'][0]['Total Marks']}")
                print(f"Obtained Marks : {r['User Result'][0]['Obtained Marks']}")


        # Exit Admin System.
        elif choice == "7":
            print("-" * 20, "Exit Admin System", "-" * 20, "\n")

            print("System Exit in 3 seconds.\n")

            def count(n):
                if n == 0:
                    return 0
                
                time.sleep(1)
                print(n)

                count(n - 1)

            count(3)

            break

# --------------------------------------------------- END ADMIN SYSTEM ---------------------------------------------------


# --------------------------------------------------- USER LOGIN SYSTEM ---------------------------------------------------

# -------------------------------------------------USER LOGIN SYSTEM FUNCTION ---------------------------------------------

def Login_Register_user():
# Runs Via Ifinite Loop.
    while True:
        print("-" * 20, "UET-ECAT Registration" ,"-" * 20,"\n")

        # QUIZZ MENU 
        main_menu = [
            "1. Login User",
            "2. Register User",
            "3. Exit"
        ]

        # Print Menu
        for menu in main_menu:
            print(menu)
        
        # Input choice from user.
        choice = input("Select option via number: ")

        # Check Choice.
        if choice in ["1", "2", "3"]:
            print("You are able to access this login system.\n")
        else:
            print("You are unable to access this login system.\n")
        

        # Login  Users.
        if choice == "1":
            print("-" * 20, "login in System" ,"-" * 20,"\n")

            print("If you are a user then you login.............\n")

            with open("Login.json", "r") as file:
                login_data = json.load(file)
            
            email = input("Enter your registered email: ")
            
            found = False
        
            for login in login_data:
                if login['Email'] == email:
                    print("Email is Verified............\n")


                user_name = input("Enter your user name: ")
                password = input("Enter your password:  ")


                if login['User Name'].lower() == user_name.lower():
                    if login['Password'] == password:

                        print("-" * 20, "login Successfull Accessed" ,"-" * 20,"\n")

                        login['Login'].append(
                            {
                            "Login Date & Time" :
                                    {
                                    "Login Date" : datetime.datetime.now().strftime("%d-%m-%Y"),
                                    "Login Time" : datetime.datetime.now().strftime("%H : %M : %S")
                                }
                            }
                        )

                        with open("Login.json", "w") as file:
                            json.dump(login_data, file, indent=4)

                        found = True
                        break

                    else:
                        print("Wrong Password. Try Again.\n")
                        continue
            
            if found == False:
                print("User Not found...........\n")

        # Register Users.
        elif choice == "2":
            print("-" * 20, "Register in System" ,"-" * 20,"\n")
            
            email = input("Enter your email: ")

            pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z]+\.[a-zA-Z]+$"
            
            # Check Email.
            if re.search(pattern, email):
                print("Valid Email")
                
            else:
                print("invalid Email. Try Again\n")
                
            with open("Login.json", "r") as file:
                login_data = json.load(file)

            email_exists = False

            for login in login_data: 
                if login['Email'] == email:
                    print("Email Exists........\n")
                    
                    email_exists = True
                    break
            
            if email_exists == False:
                print("Email Not Exists.......\n")

                user_name = input("Enter your Name: ")
                password = input("Enter your password. Password must be 8 Charaters. " \
                "Othwerwise, you enter details Again: ")

                if len(password) < 6:
                    print("Password must be greater than 6 characters.\n")
                    continue
                else: 
                    print("Your password is Fullfil our demands.\n")

                

                time.sleep(3)
                
                
                register = {
                    "User ID" : str(uuid.uuid4),
                    "User Name" : user_name,
                    "Email" : email,
                    "Password" : password,
                    "Login" : []
                }

                login_data.append(register)

                with open("Login.json", "w") as file:
                    json.dump(login_data, file, indent=4)
            
                print("-" * 20, "User Registered Successfully" ,"-" * 20,"\n")

                time.sleep(3)
                os.system("cls" if os.name == 'nt' else "clear")

    # Exit System.
        elif choice == "3":
            print("-" * 20, "Exit Program" ,"-" * 20,"\n")
            
            print("Login, Register System exit in 3 seconds............\n")

            def count(n):

                if n == 0:
                    return 0
                
                time.sleep(1)
                print(n)
                
                count(n - 1)

            count(3)
            print("System Exit Successfully.......\n")
            break


# -------------------------------------------------------END USER LOGIN OR REGISTERED SYSTEM ------------------------------------------


# ------------------------------------------------------- ECAT TEST SYSTEM ------------------------------------------------------------

def ecat_section(user_name, user_email):
    print("-" * 20,"You are now in ECAT SECTION", "-" * 20, "\n")

# SELECT SUBJECTS 

    with open("Quizz.json", "r") as file:
        quizz_data = json.load(file)
    
    

    selected_sections = []

    for i in range(3):

        while True:

            section = input(
                f"Enter Subject according to your choice {i+1}: "
            ).title()

            if section == "English":
                print("English is compulsory. Select another subject.\n")
                continue

            if section in selected_sections:
                print("Section already selected.\n")
                continue

            selected_sections.append(section)
            break

# Add English compulsory
    selected_sections.append("English")

# LOAD QUESTIONS.

    all_questions = []

    section_exists = False

    for sec in quizz_data:
        if sec['Section'].lower() in [s.lower()
            for s in selected_sections]:
            section_exists = True

            if sec['Section'] == "English":
                all_questions.extend(
                    random.sample(
                        sec['Questions'],
                        min(10, len(sec['Questions']))
                    )
                )

            else:
                all_questions.extend(
                    random.sample(
                        sec['Questions'],
                        min(30, len(sec['Questions']))
                    )
                )

        print("Question Loaded: ", len(all_questions))

    if not section_exists:
        print("Section not Exists.\n")
        return

# SHUFFLE QUESTIONS.
    random.shuffle(all_questions)

# ECAT TEST START.
    total_questions = len(all_questions)

    correct = 0
    wrong = 0

    questions_solved = 0
    halfway_prompt_shown = False

    test_time = 100 * 60  # 100 minutes
    start_time = time.time()

# Quiz questions here
    for q in all_questions:

        remaining = test_time - (time.time() - start_time)

        if remaining <= 0:
            print("\nTime Over!")
            break

        mins = int(remaining // 60)
        secs = int(remaining % 60)

        print(f"\nTime Left: {mins:02}:{secs:02}")

        print("\n" + q['Question'])

        for key, value in q['Options'].items():
            print(f"{key}. {value}")

        answer = input("Select Option (A/B/C/D): ").upper()

        questions_solved += 1

        if answer == q['Correct Answer']:
            correct += 1
        else:
            wrong += 1

        elapsed = time.time() - start_time

        if (
            not halfway_prompt_shown
            and (
                questions_solved >= total_questions * 0.5
                or elapsed >= test_time * 0.5
            )
        ):
            halfway_prompt_shown = True

            print("\n50% of the test has been completed.")

            choice = input(
                "Do you want to continue solving all questions? (y/n): "
            )

            if choice.lower() == "n":
                print("Test Submitted.")
                break
            
# CALCULATE RESULT
    
    total_questions = len(all_questions)
    total_marks = total_questions * 4

    obtained_marks = (correct * 4) - (wrong * 5)

    marks = max(0, obtained_marks)

# VIEW RESULT
# READ ALL FILES
    with open("Login.json", "r") as file:
        login_data = json.load(file)

    user_found = False

    for login in login_data:
        if login['Email'].lower() == user_email.lower():

            try:
                with open("Result.json", "r") as file:
                    result_data = json.load(file)
            except:
                result_data = []

            user_found = True

            User_ID = login["User ID"]

            Result = {
                "USER ID": User_ID,
                "User Name": user_name,
                "User Email": user_email,
                "User Result": [
                        {
                        "Total Questions": total_questions,
                        "Total Marks": total_marks,
                        "Obtained Marks": marks
                    }
                ]
            }

            result_data.append(Result)

            with open("Result.json", "w") as file:
                json.dump(result_data, file, indent=4)

            break

    if not user_found:
        print("User ID not found.\n")
    
# View Result

    with open("Result.json", "r") as file:
        result_data = json.load(file)

    for r in result_data:
        if r["User Email"].lower() == user_email.lower():
            
            print("-" * 60, "\n")
            print("ECAT RESULT\n")
            print("-" * 60, "\n")

            print(f"User Name      : {r['User Name']}")
            print(f"User Email     : {r['User Email']}")
            print(f"Total Questions: {r['User Result'][0]['Total Questions']}")
            print(f"Total Marks    : {r['User Result'][0]['Total Marks']}")
            print(f"Obtained Marks : {r['User Result'][0]['Obtained Marks']}")


# -------------------------------------------------END ECAT TEST SYSTEM ------------------------------------------------


# --------------------------------------------- ECAT TEST LOGIN FUNCTION ------------------------------------------------

def ecat_test():
    print("First you Login, then you will start ECAT Test.\n")

    with open("Login.json", "r") as file:
        login_data = json.load(file)

    email = input("Enter your registered email: ")

    login_exists = False

    for login in login_data:

        if login['Email'].lower() == email.lower():

            login_exists = True

            print("Email Verified Successfully.\n")

            name = input("Enter your User Name: ")
            password = input("Enter your password: ")

            if (
                login['User Name'].lower() == name.lower()
                and login['Password'] == password
            ):

                print("Details matching. Please wait.\n")

                login['Login'].append(
                    {
                        "Login Date & Time": {
                            "Login Date": datetime.datetime.now().strftime("%d-%m-%Y"),
                            "Login Time": datetime.datetime.now().strftime("%H:%M:%S")
                        }
                    }
                )

                with open("Login.json", "w") as file:
                    json.dump(login_data, file, indent=4)

                ecat_section(name, email)

                return
            
            else:
                print("Invalid username and password.\n")

    if not login_exists:
        print("User not found")


# ----------------------------------------------- END ECAT TEST LOGIN FUNCTION ------------------------------------------



# ------------------------------------------------ TEST MENU SELECTION -------------------------------------------------

Total_menu = [
    "1. Register Admin",
    "2. Register User",
    "3. ECAT Test",
    "4. Exit"
    ]

for menu in Total_menu:
    print(menu)


choice = input("Select option via number: ")

if choice in ["1", "2", "3", "4"]:
    print("You are able to Access this system.\n")
else:
    print("You are unable to access tihs system\n")


# ----------------------------------------------- END TEST MENU SECTION -------------------------------------------------


# ---------------------------------------------- CHOICES OF SECTION -----------------------------------------------------


# ---------------------------------------------- REGISTER ADMIN SECTION -------------------------------------------------
exists = False

for a in admin_data:
    if a.get("Admin Name") == "Zargham - Ullah":
        exists = True
        break

if not exists:

    admin = {
        "Admin Id": str(uuid.uuid4()),
        "Admin Name": "Zargham - Ullah",
        "Password": "1234_qwe@"
    }

    admin_data.append(admin)

    with open("Admin.json", "w") as file:
        json.dump(admin_data, file, indent=4)
    
# Registered Admin.
if choice == "1":
    print("-" * 20, "This section only for Registered Admin", "-" * 20, "\n")

    with open("Admin.json", "r") as file:
        data = json.load(file)

    def admin_key():

        secret_key = input("Enter Secret Key: ")

        if secret_key != "UET-ECAT-ADMIN":
            print('Access Denied')
            return False
        
        return True
    
    if not admin_key():
        exit()

    
    # Admin Login Section.
    admin_name = input("Enter Admin Name: ")
    password = input("Enter Admin Password: ")

    found = False

    for admin in data:
        if admin['Admin Name'].lower() == admin_name.lower():
            if admin['Password'] == password:

                print("Admin Login Successfull.\n")
                Admin_Register_Login()
                
                found = True
    
    if not found:
        print("Admin Not Found.\n")
        

# ------------------------------------------------ END REGISTER ADMIN SECTION ---------------------------------------


# ------------------------------------------------ REGISTER USER SECTION --------------------------------------------

if choice == "2":
    print("-" * 20, "Register User / Login Section", "-" * 20, "\n")

    Login_Register_user()


# ---------------------------------------------- END REGISTER ADMIN SECTION -----------------------------------------


# ---------------------------------------------- LLOGIN FOR TEST ----------------------------------------------------


if choice == "3":
    print("-" * 20, "ECAT TEST SECTION", "-" * 20, "\n")

    ecat_test()