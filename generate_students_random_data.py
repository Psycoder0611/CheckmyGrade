import csv, random

COURSE_IDS = ["DATA200", "DATA201", "DATA202"]

with open('students.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['email_address','first_name','last_name','course_id','grade','marks'])
    
    for i in range(1, 1001):  # will generate 1000 students
        email = f"student{i}@mycsu.edu"
        fname = f"First{i}"
        lname = f"Last{i}"
        
        # Randomly assign one of your chosen courses
        course = random.choice(COURSE_IDS)
        
        marks = random.randint(0, 100)

        # Assign grade based on marks
        if marks >= 97:
            grade = "A+"
        elif marks >= 93:
            grade = "A"
        elif marks >= 90:
            grade = "A-"
        elif marks >= 87:
            grade = "B+"
        elif marks >= 83:
            grade = "B"
        elif marks >= 80:
            grade = "B-"
        elif marks >= 77:
            grade = "C+"
        elif marks >= 73:
            grade = "C"
        elif marks >= 70:
            grade = "C-"
        elif marks >= 60:
            grade = "D"
        else:
            grade = "F"

        writer.writerow([email, fname, lname, course, grade, marks])

print("Successfully created students.csv with 1000 random records!")
