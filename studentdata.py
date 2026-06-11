import csv
import hashlib
from datetime import datetime

#STORAGE STRUCTURES
system_users = []  # Stores username & password hash for authentication
registered_usernames = set()
active_students = [] #active student
trash = [] #students removed 
registered_phones = set() #phone numbers which are registered

#UTILITY FUNCTIONS
#CALCULATE AGE -
def calculate_age(dob_string):
    birth_date = datetime.strptime(dob_string, "%d-%m-%Y")
    today = datetime.today()
    
    # AGE CALCULATION (Birthday has occured)
    age = today.year - birth_date.year
    
    # (Birthday has not occured)
    has_birthday_passed = (today.month, today.day) >= (birth_date.month, birth_date.day)
    if not has_birthday_passed:
        age -= 1
        
    return age

#PHONE NUMBER VALIDATION:
def get_valid_phone():
    while True:
        phone = input("Enter Phone Number: ").strip()
        
        # ONLY NUMBERS:
        if not phone.isdigit():
            print("Invalid Input!")
            continue
            
        # 10 DIGITS:
        if len(phone) != 10:
            print("Invalid Input!")
            continue
            
        # PHONE NUMBER ISN'T PREVIOUSLY REGISTERED:
        if phone in registered_phones:
            print("This number is already registered!")
            continue
            
        return phone

#DOB VALIDATION:
def get_valid_date():
    while True:
        dob_input = input("Enter Date of Birth (DD-MM-YYYY): ").strip()
        try:
            # 1. Tries to parse the format; fails if invalid date or bad format
            birth_date = datetime.strptime(dob_input, "%d-%m-%Y")
            
            # 2. Calculate a tentative age right here to check boundaries
            today = datetime.today()
            age = today.year - birth_date.year
            
            # Adjust age downward if the birthday hasn't happened yet this year
            has_birthday_passed = (today.month, today.day) >= (birth_date.month, birth_date.day)
            if not has_birthday_passed:
                age -= 1
            
            #AGE RANGE CHECKS:
            if age < 0:
                print(f"Invalid Age!")
                continue  # Restarts the loop
                
            if age > 125:
                print(f"Invalid Age! Please enter real age.")
                continue  # Restarts the loop
            
            return dob_input
            
        except ValueError:
            print("Invalid Format! Please enter date in DD-MM-YYYY format.")

#PASSWORD HASHING:
def hash_password(password_string):
    return hashlib.sha256(password_string.encode()).hexdigest() #SHA-256 : Secure HAsh Algo 256 bit hash output

#FEATURE FUNCTIONS:
#ADD STUDENT:
def add_student():
    print("\n Add New Student ")
    name = input("Enter Full Name: ").strip()
    
    # For Empty Name -
    if not name:
        print("Please enter a valid name!")
        return

    dob = get_valid_date()
    phone = get_valid_phone()
    age = calculate_age(dob)
    
    # Student Record dictionary
    student_record = {
        "name": name,
        "dob": dob,
        "age": age,
        "phone": phone
    }

    active_students.append(student_record)
    registered_phones.add(phone)
    print(f"Success! {name} (Age: {age}) has been added.")

#SEARCH STUDENT:
def search_student():
    print("\n Search Student Directory :")
    print("1. Search by Name")
    print("2. Search by Phone Number")
    choice = input("Select 1 or 2: ").strip()
    
    found_any = False
    
    #Search by Name - Case insensitive, Parital match"
    if choice == "1":
        query = input("Enter name: ").strip().lower()
        print("\n Search Results ")
        for student in active_students:
            if query in student["name"].lower():
                print(f"Name: {student['name']} | Age: {student['age']} | Phone: {student['phone']} | DOB: {student['dob']}")
                found_any = True

    #Seach by Phone Number           
    elif choice == "2":
        query = input("Enter phone number to search: ").strip()
        print("\n Search Results ")
        for student in active_students:
            if student["phone"] == query:
                print(f"Name: {student['name']} | Age: {student['age']} | Phone: {student['phone']} | DOB: {student['dob']}")
                found_any = True
                break # Phone numbers are unique so there is no need to keep looping
    else:
        print("Invalid Choice")
        return

    if not found_any:
        print("No active student matching your search")

#FILTER STUDENTS BY AGE:
def filter_by_age():
    print("\n Filter Students By Age Range ")
    try:
        min_age = int(input("Enter Minimum Age: "))
        max_age = int(input("Enter Maximum Age: "))
    except ValueError:
        print("Please enter valid integers for ages!")
        return
        
    print(f"\n Active Students Between Ages {min_age} and {max_age} ")
    found_any = False
    for student in active_students:
        if min_age <= student["age"] <= max_age:
            print(f"{student['name']} (Age: {student['age']}) - Phone: {student['phone']}")
            found_any = True
            
    if not found_any:
        print("No students found.")

#DELETE STUDENTS
def delete_management_menu():
    while True:
        print("\n Delete or Manage Student: ")
        print("1. Remove Student temporarily")
        print("2. View Trash Bin Items")
        print("3. Restore Student From Trash")
        print("4. Delete Student Permanently")
        print("5. Return to Main Menu")
        
        choice = input("Select operation (1-5): ").strip()
        
        #TEMORARY DELETE - Using Phone number
        if choice == "1":
            phone = input("Enter the Phone Number of the student to remove: ").strip()
            target_student = None
            
            # Look up student in active directory
            for student in active_students:
                if student["phone"] == phone:
                    target_student = student
                    break
            
            if target_student:
                active_students.remove(target_student)
                trash.append(target_student)
                print(f"{target_student['name']} has been moved to Trash Bin.")
            else:
                print("No active student found with that phone number.")

        #VIEW TRASH BIN        
        elif choice == "2":
            print("\n Trash Bin Students")
            if not trash:
                print(" Trash is empty.")
            for student in trash:
                print(f"[Archived] {student['name']} - Phone: {student['phone']}")

        #RESTORE STUDENT FROM TRASH        
        elif choice == "3":
            phone = input("Enter the Phone Number of the student to restore: ").strip()
            target_student = None
            
            for student in trash:
                if student["phone"] == phone:
                    target_student = student
                    break
                    
            if target_student:
                trash.remove(target_student)
                active_students.append(target_student)
                print(f"Restored {target_student['name']} successfully!")
            else:
                print("That student profile does not exist in the Trash Bin.")

        #PERMANENTLY DELETE STUDENT         
        elif choice == "4":
            phone = input("Enter Phone Number to permanently delete: ").strip()
            target_student = None
            found_in_trash = False
            
            # Search active lists
            for student in active_students:
                if student["phone"] == phone:
                    target_student = student
                    break
            
            # Search trash, if not found in active list
            if not target_student:
                for student in trash:
                    if student["phone"] == phone:
                        target_student = student
                        found_in_trash = True
                        break
            
            if target_student:
                if found_in_trash:
                    trash.remove(target_student)
                else:
                    active_students.remove(target_student)
                
                # Free up the phone number allocation from our validator Set
                registered_phones.remove(phone)
                print(f"{target_student['name']} deleted from permanently memory.")
            else:
                print("No profile found matching that phone number anywhere in memory.")
                
        elif choice == "5":
            break
        else:
            print("Selection out of range.")

#CREATING USER ACCOUNT: 
def create_user_account():
    print("\n Create Admin Account ")
    while True:
        username = input("Enter a new username: ").strip().lower()
        if not username:
            print("Username cannot be blank.")
            continue
        if username in registered_usernames:
            print("Username not available!")
            continue
        break
        
    dob = get_valid_date() 
    password = input("Enter a secure password: ").strip()
    while not password:
        print("Password cannot be blank.")
        password = input("Enter a secure password: ").strip()
        
    user_account = {
        "username": username,
        "password_hash": hash_password(password),
        "dob": dob
    }
    system_users.append(user_account)
    registered_usernames.add(username)
    print(f"Account successfully created")


def change_password():
    print("\n Change Password Portal ")
    username = input("Enter username: ").strip().lower()
    dob_input = input("Enter your registered Date of Birth (DD-MM-YYYY): ").strip()
    
    target_user = None
    for user in system_users:
        if user["username"] == username:
            target_user = user
            break
            
    if not target_user:
        print("Username not found.")
        return

    if target_user["dob"] != dob_input:
        print("Date of Birth does not match.")
        return
        
    # Validation Passed -> Proceed to change password
    print("Identity Verified Successfully.")
    new_password = input("Enter your new secure password: ").strip()
    while not new_password:
        print("Password cannot be blank.")
        new_password = input("Enter your new secure password: ").strip()
        
    target_user["password_hash"] = hash_password(new_password)
    print("Success! Your password has been updated. Please log in again.")

#USER AUTHENTICATION:
def authenticate_user():
    while True:
        print(" SYSTEM SECURITY GATEWAY ")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Forgot Password")
        print("4. Exit Application")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            print("\n Account Login ")
            username = input("Enter username: ").strip().lower()
            password = input("Enter password: ").strip()
            
            input_hash = hash_password(password)
            login_success = False
            
            for user in system_users:
                if user["username"] == username and user["password_hash"] == input_hash:
                    login_success = True
                    break
            
            if login_success:
                print(f"Access Granted!")
                return True
            else:
                print("Invalid username or password!")
                
        elif choice == "2":
            create_user_account()
        elif choice == "3":
            change_password()
        elif choice == "4":
            print("\n System closing down. Goodbye!")
            exit()
        else:
            print("Invalid selection. Please enter a number between 1 and 4.")

#IMPORT STUDENTS FROM CSV
def import_students_from_csv():
    print("\n Import Students from CSV File ")
    filename = "students.csv"
    
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            # DictReader uses the first row as keys for each column
            reader = csv.DictReader(file)
            
            # Verify:
            expected_headers = {"Name", "DOB", "Phone"}
            if not reader.fieldnames or not expected_headers.issubset(set(reader.fieldnames)):
                print("CSV Structure Error! The file must contain columns: Name, DOB, Phone")
                return
               
            success_count = 0
            skipped_count = 0
            row_number = 1  # Tracks rows
            
            for row in reader:
                row_number += 1
                
                # Extract and clean values
                name = row["Name"].strip() if row["Name"] else ""
                dob_str = row["DOB"].strip() if row["DOB"] else ""
                phone = row["Phone"].strip() if row["Phone"] else ""
                
                # Empty fields
                if not name or not dob_str or not phone:
                    print(f"Row {row_number} Skipped: Missing fields (Name/DOB/Phone).")
                    skipped_count += 1
                    continue
                try:
                    birth_date = datetime.strptime(dob_str, "%d-%m-%Y")
                    today = datetime.today()
                    age = today.year - birth_date.year
                    has_birthday_passed = (today.month, today.day) >= (birth_date.month, birth_date.day)
                    if not has_birthday_passed:
                        age -= 1

                    if age < 0 or age > 125:
                        print(f"Row {row_number} Skipped: Age ({age}) is out of human limits (0-125).")
                        skipped_count += 1
                        continue
                        
                except ValueError:
                    print(f"Row {row_number} Skipped: Invalid Date format '{dob_str}'. Must be DD-MM-YYYY.")
                    skipped_count += 1
                    continue
                
                # Check phone numbers
                if not phone.isdigit() or len(phone) != 10:
                    print(f"Row {row_number} Skipped: Check Phone number - '{phone}'")
                    skipped_count += 1
                    continue
                
                # Duplicate phone number
                if phone in registered_phones:
                    print(f"Row {row_number} Skipped: Phone number '{phone}' already exists in database registry.")
                    skipped_count += 1
                    continue

                student_record = {
                    "name": name,
                    "dob": dob_str,
                    "age": age,
                    "phone": phone
                }
                
                active_students.append(student_record)
                registered_phones.add(phone)
                success_count += 1
                
            print(" BULK IMPORT COMPLETION ")
            print(f"Successfully Imported : {success_count} students.")
            print(f"Rejected : {skipped_count} invalid rows.")
            
    except FileNotFoundError:
        print(f"Operation Failed: The file '{filename}' was not found.")

#MAIN MENU - CLI
def main():
    authenticate_user()
    while True:
        print(" STUDENT DATA MANAGEMENT SYSTEM ")
        print("1. Add Student Record")
        print("2. Search Student Directory")
        print("3. Filter Students by Age")
        print("4. Delete & Recovery Operations Menu")
        print("5. Import Students from CSV File")
        print("6. Exit")
        
        main_choice = input("Please select (1-6): ").strip()
        
        if main_choice == "1":
            add_student()
        elif main_choice == "2":
            search_student()
        elif main_choice == "3":
            filter_by_age()
        elif main_choice == "4":
            delete_management_menu()
        elif main_choice == "5":
            import_students_from_csv() 
        elif main_choice == "6":
            print("\nSystem shut down successfully. Goodbye!")
            break
        else:
            print("Invalid menu choice! Please select an option between 1 and 6.")

if __name__ == "__main__":
    main()