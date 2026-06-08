from datetime import datetime

#STORAGE STRUCTURES
active_students = [] #dictionary of active student
trash = [] #students who were removed 
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

#MAIN MENU - CLI
def main():
    while True:
        print("     STUDENT DATA MANAGEMENT SYSTEM       ")
        print("1. Add Student Record")
        print("2. Search Student Directory")
        print("3. Filter Students by Age")
        print("4. Delete & Recovery Operations Menu")
        print("5. Close Program")
        
        main_choice = input("Please select (1-5): ").strip()
        
        if main_choice == "1":
            add_student()
        elif main_choice == "2":
            search_student()
        elif main_choice == "3":
            filter_by_age()
        elif main_choice == "4":
            delete_management_menu()
        elif main_choice == "5":
            print("\n System shut down successfully. Thankyou!")
            break
        else:
            print("Invalid menu choice! Please select an option between 1 and 5.")

if __name__ == "__main__":
    main()