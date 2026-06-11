STUDENT DATA MANAGEMENT SYSTEM :

DAY 1 - Building the Student Data Management System :

Imported - datetime 
Storage structures : active students, trash, registered phone numbers 
Utility functions : age calculation (by DOB), Phone number validation, DOB Validation 
Feature functions : Add student, Search student (by name & phone number), Filter students by age, Delete Students (Temporarily (in trash), Permanently)

DAY 2 - Adding User Authentication :

Storage structures : system users, reg usernames 
Import - hashlib 
Utility functions : Creating user account (username, password) - password secured using SHA256, User Authentication (Login, Sign Up)

DAY 3 - Adding Forgot Password Option :

The system asks for DOB while creating user account along with username and password. 
Utility function changes : Creating user account (username, DOB, password), User authentication (Login, Sign UP, Forgot Password). 
When user enters forgot password - the system asks for username and DOB. If matches then allows to create new password.

DAY 4 - Importing Students from csv file

Import csv 
Feature function : Import students from csv file
Takes student info from file named students.csv and then verifies the format and whether the information is valid or not. Then adds them into system.

