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
