MAIN MENU - 
Add Student
Search Student (Name/Number)
Filter by Age
Delete & Recover
Close

ADD STUDENT 
Ask for Name - Stores name : Case insensitive
Ask for DOB (DD-MM-YYYY) : Checks Format, Checks Year (Range 0:125) - Stores DOB 
Using DOB, Calculates Age - using datetime library - stores age (AGE function) - Subtract dob from current date to get age
Ask for Number : Checks 10 digits, only integers - Stores in registered phone numbers list
Stores all this info in a dictionary, which is stored in a list called Active Student

SEARCH STUDENT 
Search by name or number
Name - Makes case insensitive, then searches for substring in names
Number - Matches number exact

FILTER BY AGE 
Age range in asked
All students falling in range are filtered (min < age < max)

DELETE & MANAGE -
Remove student temporarily - takes phone number and removes student from active list and adds them to trash bin lis - SOFT
Checks Trash Bin items
Restore student back from Trash bin to Active List
Completely delete from database (Remove from active list and added no where) - HARD
