import csv
import os
import time
from datetime import datetime
import hashlib

#BASE/ENTITY Classes
class Student:
    def __init__(self, email_address, first_name, last_name, course_id="", grade="", marks=0):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = marks

    def display_record(self):
        print(f"Email: {self.email_address}, Name: {self.first_name} {self.last_name}, "
            f"Course: {self.course_id}, Grade: {self.grade}, Marks: {self.marks}")
      
    def to_dict(self):
        return {
            'email_address': self.email_address,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'course_id': self.course_id,
            'grade': self.grade,
            'marks': self.marks
        }


class Course:
    def __init__(self, course_id, course_name, description=""):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
    
    def display_course(self):
        print(f"Course ID: {self.course_id}, Name: {self.course_name}, Description: {self.description}")

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'description': self.description
        }


class Professor:
    def __init__(self, professor_id, professor_name, rank, course_id):
        self.professor_id = professor_id
        self.professor_name = professor_name
        self.rank = rank
        self.course_id = course_id

    def display_professor(self):
        print(f"Professor ID: {self.professor_id}, Name: {self.professor_name}, "
              f"Rank: {self.rank}, Course: {self.course_id}")

    def to_dict(self):
        return {
            'professor_id': self.professor_id,
            'professor_name': self.professor_name,
            'rank': self.rank,
            'course_id': self.course_id
        }

class Grade:
    """Grade class defines grade scale (A, B, C with mark ranges)"""
    def __init__(self, grade_id, grade_letter, min_marks, max_marks):
        self.grade_id = grade_id
        self.grade_letter = grade_letter
        self.min_marks = min_marks
        self.max_marks = max_marks
    
    def is_in_range(self, marks):
        """Check if marks fall in this grade range"""
        return self.min_marks <= marks <= self.max_marks
    
    def display_grade(self):
        print(f"Grade: {self.grade_letter} ({self.min_marks}-{self.max_marks} marks)")
    
    def to_dict(self):
        return {
            'grade_id': self.grade_id,
            'grade_letter': self.grade_letter,
            'min_marks': self.min_marks,
            'max_marks': self.max_marks
        }

class LoginUser: 
    def __init__(self, email_id, password, role):
        self.email_id = email_id
        self.password = password # Stored as encrypted hash
        self.role = role   

    def encrypt_password(self, password):
        """
        Encrypt password using SHA-256 one-way hashing
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, encrypted):
        """
        Verify password against encrypted hash
        Instead of decrypting, we hash the input and compare
        """
        return self.encrypt_password(password) == encrypted
    
    def to_dict(self):
        """Convert user to dictionary for CSV"""
        return {
            'user_id': self.email_id,
            'password': self.password,
            'role': self.role
        }


# Manager Classes
class StudentManager:
    """Manages all student operations"""
    def __init__(self, csv_file='students.csv'):
        self.csv_file = csv_file
        self.students = []
        self.load_from_csv()
    
    def load_from_csv(self):
        """Load students from CSV file"""
        if not os.path.exists(self.csv_file):
            return
        
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student = Student(
                        row['email_address'],
                        row['first_name'],
                        row['last_name'],
                        row['course_id'],
                        row['grade'],
                        int(row['marks']) if row['marks'] else 0
                    )
                    self.students.append(student)
            print(f"✓ Loaded {len(self.students)} students from {self.csv_file}")
        except Exception as e:
            print(f"Error loading students: {e}")

    def save_to_csv(self):
        """Save students to CSV file"""
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['email_address', 'first_name', 'last_name', 'course_id', 'grade', 'marks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students:
                    writer.writerow(student.to_dict())
        except Exception as e:
            print(f"Error saving students: {e}")
    
    def validate_email(self, email):
        # Check if email has @ and a dot after @
        if '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        if '.' not in parts[1]:
            return False
        if len(parts[0]) == 0 or len(parts[1]) == 0:
            return False
        return True
    
    def validate_marks(self, marks):
        """Validate marks range"""
        return 0 <= marks <= 100
    
    def add_student(self, student):
        """Add new student with validation"""
        # Validation
        if not student.email_address or not self.validate_email(student.email_address):
            print("Invalid email address format!")
            return False
        
        if not student.first_name or not student.last_name:
            print("First name and last name are required!")
            return False
        
        if not self.validate_marks(student.marks):
            print("Marks must be between 0 and 100!")
            return False
        
        if any(s.email_address == student.email_address for s in self.students):
            print(f"Student with email {student.email_address} already exists!")
            return False
        
        self.students.append(student)
        self.save_to_csv()
        print(f"Student {student.first_name} {student.last_name} added successfully!")
        return True             

    def delete_student(self, email_address):
        """Delete student by email"""
        initial_count = len(self.students)
        self.students = [s for s in self.students if s.email_address != email_address]
        
        if len(self.students) < initial_count:
            self.save_to_csv()
            print(f"Student with email {email_address} deleted successfully!")
            return True
        else:
            print(f"Student with email {email_address} not found!")
            return False
    
    def update_student(self, email_address, **kwargs):
        """Update student details"""
        for student in self.students:
            if student.email_address == email_address:
                # Validate marks if being updated
                if 'marks' in kwargs:
                    if not self.validate_marks(kwargs['marks']):
                        print("Marks must be between 0 and 100!")
                        return False
                
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_to_csv()
                print(f"Student {email_address} updated successfully!")
                return True

        print(f"Student with email {email_address} not found!")
        return False
    
    def search_student(self, email_address):
        """Search for a student by email and measure performance"""
        start_time = time.time()
        result = None
        
        for student in self.students:
            if student.email_address == email_address:
                result = student
                break
        
        elapsed_time = time.time() - start_time
        
        if result:
            print("\n" + "="*80)
            result.display_record()
            print("="*80)
        else:
            print(f"Student with email {email_address} not found!")
        
        print(f"Search completed in {elapsed_time:.6f} seconds")
        return result, elapsed_time
    
    def sort_students(self, by='email', ascending=True):
        """Sort students by email, marks, or name"""
        start_time = time.time()
        
        if by == 'email':
            self.students.sort(key=lambda s: s.email_address, reverse=not ascending)
        elif by == 'marks':
            self.students.sort(key=lambda s: s.marks, reverse=not ascending)
        elif by == 'name':
            self.students.sort(key=lambda s: (s.last_name, s.first_name), reverse=not ascending)
        else:
            print("Invalid sort option!")
            return 0
        
        elapsed_time = time.time() - start_time
        print(f"Students sorted by {by} ({'ascending' if ascending else 'descending'})")
        print(f"Sort completed in {elapsed_time:.6f} seconds")
        return elapsed_time
    
    def display_all_students(self):
        """Display all students"""
        if not self.students:
            print("No students found!")
            return
        
        print(f"\n{'='*80}")
        print(f"Total Students: {len(self.students)}")
        print(f"{'='*80}")
        for student in self.students:
            student.display_record()
        print(f"{'='*80}")
    
    def get_statistics(self, course_id=None):
        """Get average and median marks for course or overall"""
        students_to_analyze = self.students
        
        if course_id:
            students_to_analyze = [s for s in self.students if s.course_id == course_id]
        
        if not students_to_analyze:
            print("No students found for statistics!")
            return None, None
        
        marks_list = [s.marks for s in students_to_analyze]
        average = sum(marks_list) / len(marks_list)
        
        sorted_marks = sorted(marks_list)
        n = len(sorted_marks)
        median = sorted_marks[n//2] if n % 2 == 1 else (sorted_marks[n//2-1] + sorted_marks[n//2]) / 2
        
        return average, median


class CourseManager:
    """Manages all course operations"""
    def __init__(self, csv_file='courses.csv'):
        self.csv_file = csv_file
        self.courses = []
        self.load_from_csv()
    
    def load_from_csv(self):
        """Load courses from CSV file"""
        if not os.path.exists(self.csv_file):
            return
        
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course = Course(row['course_id'], row['course_name'], row['description'])
                    self.courses.append(course)
            print(f"Loaded {len(self.courses)} courses from {self.csv_file}")
        except Exception as e:
            print(f"Error loading courses: {e}")
    
    def save_to_csv(self):
        """Save courses to CSV file"""
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['course_id', 'course_name', 'description']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for course in self.courses:
                    writer.writerow(course.to_dict())
        except Exception as e:
            print(f"Error saving courses: {e}")
    
    def add_course(self, course):
        """Add new course"""
        if not course.course_id:
            print("Course ID is required!")
            return False
        
        if any(c.course_id == course.course_id for c in self.courses):
            print(f"Course with ID {course.course_id} already exists!")
            return False
        
        self.courses.append(course)
        self.save_to_csv()
        print(f"Course {course.course_name} added successfully!")
        return True
    
    def delete_course(self, course_id):
        """Delete course by ID"""
        initial_count = len(self.courses)
        self.courses = [c for c in self.courses if c.course_id != course_id]
        
        if len(self.courses) < initial_count:
            self.save_to_csv()
            print(f"Course {course_id} deleted successfully!")
            return True
        else:
            print(f"Course {course_id} not found!")
            return False
    
    def display_all_courses(self):
        """Display all courses"""
        if not self.courses:
            print("No courses found!")
            return
        
        print(f"\n{'='*80}")
        print(f"Total Courses: {len(self.courses)}")
        print(f"{'='*80}")
        for course in self.courses:
            course.display_course()
        print(f"{'='*80}")


class ProfessorManager:
    """Manages all professor operations"""
    def __init__(self, csv_file='professors.csv'):
        self.csv_file = csv_file
        self.professors = []
        self.load_from_csv()
    
    def load_from_csv(self):
        """Load professors from CSV file"""
        if not os.path.exists(self.csv_file):
            return
        
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    professor = Professor(
                        row['professor_id'],
                        row['professor_name'],
                        row['rank'],
                        row['course_id']
                    )
                    self.professors.append(professor)
            print(f"Loaded {len(self.professors)} professors from {self.csv_file}")
        except Exception as e:
            print(f"Error loading professors: {e}")
    
    def save_to_csv(self):
        """Save professors to CSV file"""
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['professor_id', 'professor_name', 'rank', 'course_id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for professor in self.professors:
                    writer.writerow(professor.to_dict())
        except Exception as e:
            print(f"Error saving professors: {e}")

    def add_professor(self, professor):
        """Add new professor"""
        if not professor.professor_id:
            print("Professor ID is required!")
            return False
        
        if any(p.professor_id == professor.professor_id for p in self.professors):
            print(f"Professor with ID {professor.professor_id} already exists!")
            return False
        
        self.professors.append(professor)
        self.save_to_csv()
        print(f"Professor {professor.professor_name} added successfully!")
        return True
    
    def delete_professor(self, professor_id):
        """Delete professor by ID"""
        initial_count = len(self.professors)
        self.professors = [p for p in self.professors if p.professor_id != professor_id]
        
        if len(self.professors) < initial_count:
            self.save_to_csv()
            print(f"Professor {professor_id} deleted successfully!")
            return True
        else:
            print(f"Professor {professor_id} not found!")
            return False

    def display_all_professors(self):
        """Display all professors"""
        if not self.professors:
            print("No professors found!")
            return
        
        print(f"\n{'='*80}")
        print(f"Total Professors: {len(self.professors)}")
        print(f"{'='*80}")
        for professor in self.professors:
            professor.display_professor()
        print(f"{'='*80}")


class GradeManager:
    """Manages grading scale and grade calculations"""
    def __init__(self, csv_file='grades.csv'):
        self.csv_file = csv_file
        self.grades = []
        self.initialize_default_grades()
        self.load_from_csv()

    def initialize_default_grades(self):
        """Initialize standard grading scale"""
        default_grades = [
            Grade("G1", "A+", 97, 100),
            Grade("G2", "A", 93, 96),
            Grade("G3", "A-", 90, 92),
            Grade("G4", "B+", 87, 89),
            Grade("G5", "B", 83, 86),
            Grade("G6", "B-", 80, 82),
            Grade("G7", "C+", 77, 79),
            Grade("G8", "C", 73, 76),
            Grade("G9", "C-", 70, 72),
            Grade("G10", "D", 60, 69),
            Grade("G11", "F", 0, 59)
        ]
        self.grades = default_grades
    
    def load_from_csv(self):
        """Load grades from CSV if exists"""
        if not os.path.exists(self.csv_file):
            self.save_to_csv()
            return
        
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.grades = []
                for row in reader:
                    grade = Grade(
                        row['grade_id'],
                        row['grade_letter'],
                        int(row['min_marks']),
                        int(row['max_marks'])
                    )
                    self.grades.append(grade)
            print(f"Loaded {len(self.grades)} grade definitions from {self.csv_file}")
        except Exception as e:
            print(f"Error loading grades: {e}")
            self.initialize_default_grades()

    def save_to_csv(self):
        """Save grades to CSV"""
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['grade_id', 'grade_letter', 'min_marks', 'max_marks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for grade in self.grades:
                    writer.writerow(grade.to_dict())
        except Exception as e:
            print(f"Error saving grades: {e}")
    
    def get_grade_for_marks(self, marks):
        """Get grade letter for given marks"""
        for grade in self.grades:
            if grade.is_in_range(marks):
                return grade.grade_letter
        return "F"
    
    def add_grade(self, grade):
        """Add new grade definition"""
        if any(g.grade_id == grade.grade_id for g in self.grades):
            print(f"Grade {grade.grade_id} already exists!")
            return False

        self.grades.append(grade)
        self.grades.sort(key=lambda g: g.min_marks, reverse=True)
        self.save_to_csv()
        print(f"Grade {grade.grade_letter} added successfully!")
        return True
    
    def delete_grade(self, grade_id):
        """Delete grade by ID"""
        initial_count = len(self.grades)
        self.grades = [g for g in self.grades if g.grade_id != grade_id]
        
        if len(self.grades) < initial_count:
            self.save_to_csv()
            print(f"Grade {grade_id} deleted!")
            return True
        else:
            print(f"Grade {grade_id} not found!")
            return False
        
    def modify_grade(self, grade_id, **kwargs):
        """Modify grade details"""
        for grade in self.grades:
            if grade.grade_id == grade_id:
                for key, value in kwargs.items():
                    if hasattr(grade, key):
                        setattr(grade, key, value)
                self.grades.sort(key=lambda g: g.min_marks, reverse=True)
                self.save_to_csv()
                print(f"✓ Grade {grade_id} modified successfully!")
                return True
        
        print(f"Grade {grade_id} not found!")
        return False

    def display_all_grades(self):
        """Display all grade definitions"""
        if not self.grades:
            print("No grades defined!")
            return
        
        print(f"\n{'='*60}")
        print(f"{'Grade Scale':^60}")
        print(f"{'='*60}")
        for grade in sorted(self.grades, key=lambda g: g.min_marks, reverse=True):
            print(f"{grade.grade_letter:5s} : {grade.min_marks:3d} - {grade.max_marks:3d} marks")
        print(f"{'='*60}")
    
    def display_grade_report(self):
        """Display detailed grade report"""
        print("\n" + "="*60)
        print(f"{'Grade Distribution Report':^60}")
        print("="*60)
        for grade in sorted(self.grades, key=lambda g: g.min_marks, reverse=True):
            grade.display_grade()
        print("="*60)


class LoginManager:
    """Manages user authentication"""
    def __init__(self, csv_file='login.csv'):
        self.csv_file = csv_file
        self.users = []
        self.load_from_csv()
    
    def load_from_csv(self):
        """Load users from CSV file"""
        if not os.path.exists(self.csv_file):
            return
        
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = LoginUser(row['user_id'], row['password'], row['role'])
                    self.users.append(user)
            print(f"Loaded {len(self.users)} users from {self.csv_file}")
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def save_to_csv(self):
        """Save users to CSV file"""
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['user_id', 'password', 'role']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for user in self.users:
                    writer.writerow(user.to_dict())
        except Exception as e:
            print(f"Error saving users: {e}")

    def register_user(self, email_id, password, role):
        """Register a new user"""
        if any(u.email_id == email_id for u in self.users):
            print(f"User {email_id} already exists!")
            return False
        
        # Create temporary LoginUser object to use encryption method
        temp_user = LoginUser(email_id, password, role)
        encrypted_password = temp_user.encrypt_password(password)
        
        # Create actual user with encrypted password
        user = LoginUser(email_id, encrypted_password, role)
        self.users.append(user)
        self.save_to_csv()
        print(f"User {email_id} registered successfully!")
        print(f"Password encrypted with SHA-256")
        return True
    
    def login(self, email_id, password):
        """Login user by verifying password"""
        for user in self.users:
            if user.email_id == email_id:
                if user.verify_password(password, user.password):
                    print(f"Login successful! Welcome {email_id} ({user.role})")
                    return True, user.role
                else:
                    print("Invalid password!")
                    return False, None
        
        print(f"User {email_id} not found!")
        return False, None
    
    def change_password(self, email_id, old_password, new_password):
        """Change user password"""
        for user in self.users:
            if user.email_id == email_id:
                if user.verify_password(old_password, user.password):
                    user.password = user.encrypt_password(new_password)
                    self.save_to_csv()
                    print("Password changed successfully!")
                    print("New password encrypted with SHA-256")
                    return True
                else:
                    print("Invalid old password!")
                    return False
        
        print(f"User {email_id} not found!")
        return False


# MAIN APPLICATION

class CheckMyGradeApp:
    """Main application class"""
    def __init__(self):
        self.student_manager = StudentManager()
        self.course_manager = CourseManager()
        self.professor_manager = ProfessorManager()
        self.grade_manager = GradeManager()
        self.login_manager = LoginManager()
        self.current_user = None
        self.current_role = None

    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print(" CheckMyGrade Application ".center(60, "="))
        print("="*60)
        print("\n🔐 Please login to continue...")
        
        # Login required
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            email = input("\nEmail: ").strip()
            password = input("Password: ").strip()
            
            success, role = self.login_manager.login(email, password)
            
            if success:
                self.current_user = email
                self.current_role = role
                break
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"⚠ {remaining} attempt(s) remaining")
        
        if not self.current_user:
            print("\nMaximum login attempts exceeded. Exiting...")
            return
        
        # Main menu loop
        while True:
            print("\n" + "="*60)
            print(f" Main Menu (Logged in as: {self.current_user}) ".center(60, "="))
            print("="*60)
            print("1. Student Management")
            print("2. Course Management")
            print("3. Professor Management")
            print("4. Grade Management")
            print("5. Reports and Statistics")
            print("6. Change Password")
            print("7. Logout and Exit")
            print("="*60)

            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.student_menu()
            elif choice == '2':
                email = input("Enter student email to delete: ").strip()
                self.student_manager.delete_student(email)
            
            elif choice == '3':
                email = input("Enter student email to update: ").strip()
                print("Enter new values (press Enter to skip):")
                updates = {}
                
                first_name = input("First name: ").strip()
                if first_name:
                    updates['first_name'] = first_name
                
                last_name = input("Last name: ").strip()
                if last_name:
                    updates['last_name'] = last_name
                
                marks = input("Marks: ").strip()
                if marks:
                    try:
                        marks_val = int(marks)
                        updates['marks'] = marks_val
                        updates['grade'] = self.grade_manager.get_grade_for_marks(marks_val)
                    except ValueError:
                        print("Invalid marks value!")
                
                if updates:
                    self.student_manager.update_student(email, **updates)
                        
            elif choice == '4':
                email = input("Enter student email to search: ").strip()
                self.student_manager.search_student(email)
            
            elif choice == '5':
                self.student_manager.display_all_students()
            
            elif choice == '6':
                print("\nSort by: 1) Email  2) Marks  3) Name")
                sort_choice = input("Enter choice: ").strip()
                order = input("Order (asc/desc): ").strip().lower()
                
                sort_by = 'email'
                if sort_choice == '2':
                    sort_by = 'marks'
                elif sort_choice == '3':
                    sort_by = 'name'
                
                self.student_manager.sort_students(by=sort_by, ascending=(order == 'asc'))
                self.student_manager.display_all_students()
            
            elif choice == '7':
                break
            else:
                print("Invalid choice!")
    
    def student_menu(self):
        #Student management menu
         while True:
            print("\n" + "="*60)
            print(" Student Management ".center(60, "-"))
            print("="*60)
            print("1. Add Student")
            print("2. Delete Student")
            print("3. Update Student")
            print("4. Search Student")
            print("5. Display All Students")
            print("6. Sort Students")
            print("7. Back to Main Menu")
            print("="*60)

            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == '1':
                try:
                    email = input("Enter student email: ").strip()
                    first_name = input("Enter first name: ").strip()
                    last_name = input("Enter last name: ").strip()
                    course_id = input("Enter course ID: ").strip()
                    marks = int(input("Enter marks (0-100): ").strip())

                    grade = self.grade_manager.get_grade_for_marks(marks)
                    student = Student(email, first_name, last_name, course_id, grade, marks)
                    self.student_manager.add_student(student)
                except ValueError:
                    print("Invalid marks! Please enter a number.")

            elif choice == '2':
                 self.course_menu()
            elif choice == '3':
                self.professor_menu()
            elif choice == '4':
                self.grade_menu()
            elif choice == '5':
                self.reports_menu()
            elif choice == '6':
                old_pass = input("Enter old password: ").strip()
                new_pass = input("Enter new password: ").strip()
                self.login_manager.change_password(self.current_user, old_pass, new_pass)
            elif choice == '7':
                print("Logging out... Goodbye!")
                break

    def course_menu(self):
        """Course management menu"""
        while True:
            print("\n" + "="*60)
            print(" Course Management ".center(60, "-"))
            print("="*60)
            print("1. Add Course")
            print("2. Delete Course")
            print("3. Display All Courses")
            print("4. Back to Main Menu")
            print("="*60)
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\n--- Add New Course ---")
                course_id = input("Enter course ID: ").strip()
                course_name = input("Enter course name: ").strip()
                description = input("Enter description: ").strip()
                
                course = Course(course_id, course_name, description)
                self.course_manager.add_course(course)
            
            elif choice == '2':
                course_id = input("Enter course ID to delete: ").strip()
                self.course_manager.delete_course(course_id)
            
            elif choice == '3':
                self.course_manager.display_all_courses()
            
            elif choice == '4':
                break
            else:
                print("Invalid choice!")
    
    def professor_menu(self):
        """Professor management menu"""
        while True:
            print("\n" + "="*60)
            print(" Professor Management ".center(60, "-"))
            print("="*60)
            print("1. Add Professor")
            print("2. Delete Professor")
            print("3. Display All Professors")
            print("4. Back to Main Menu")
            print("="*60)
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\n--- Add New Professor ---")
                prof_id = input("Enter professor email: ").strip()
                prof_name = input("Enter professor name: ").strip()
                rank = input("Enter rank: ").strip()
                course_id = input("Enter course ID: ").strip()
                
                professor = Professor(prof_id, prof_name, rank, course_id)
                self.professor_manager.add_professor(professor)
            
            elif choice == '2':
                prof_id = input("Enter professor ID to delete: ").strip()
                self.professor_manager.delete_professor(prof_id)
            
            elif choice == '3':
                self.professor_manager.display_all_professors()
            
            elif choice == '4':
                break
            else:
                print("Invalid choice!")
    
    def grade_menu(self):
        """Grade management menu"""
        while True:
            print("\n" + "="*60)
            print(" Grade Management ".center(60, "-"))
            print("="*60)
            print("1. Display Grade Scale")
            print("2. Add New Grade")
            print("3. Delete Grade")
            print("4. Modify Grade")
            print("5. Calculate Grade for Marks")
            print("6. Display Grade Report")
            print("7. Back to Main Menu")
            print("="*60)
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.grade_manager.display_all_grades()
            
            elif choice == '2':
                try:
                    print("\n--- Add New Grade ---")
                    grade_id = input("Enter grade ID: ").strip()
                    letter = input("Enter grade letter (A+, A, B, etc.): ").strip()
                    min_marks = int(input("Enter minimum marks: "))
                    max_marks = int(input("Enter maximum marks: "))
                    
                    grade = Grade(grade_id, letter, min_marks, max_marks)
                    self.grade_manager.add_grade(grade)
                except ValueError:
                    print("Invalid input! Marks must be numbers.")
            
            elif choice == '3':
                grade_id = input("Enter grade ID to delete: ").strip()
                self.grade_manager.delete_grade(grade_id)
            
            elif choice == '4':
                grade_id = input("Enter grade ID to modify: ").strip()
                print("Enter new values (press Enter to skip):")
                updates = {}
                
                letter = input("Grade letter: ").strip()
                if letter:
                    updates['grade_letter'] = letter
                
                min_marks = input("Minimum marks: ").strip()
                if min_marks:
                    try:
                        updates['min_marks'] = int(min_marks)
                    except ValueError:
                        print("Invalid minimum marks!")
                
                max_marks = input("Maximum marks: ").strip()
                if max_marks:
                    try:
                        updates['max_marks'] = int(max_marks)
                    except ValueError:
                        print("Invalid maximum marks!")
                
                if updates:
                    self.grade_manager.modify_grade(grade_id, **updates)
            
            elif choice == '5':
                try:
                    marks = int(input("Enter marks: "))
                    grade_letter = self.grade_manager.get_grade_for_marks(marks)
                    print(f"✓ Marks {marks} = Grade {grade_letter}")
                except ValueError:
                    print("Invalid marks!")
            
            elif choice == '6':
                self.grade_manager.display_grade_report()
            
            elif choice == '7':
                break
            else:
                print("Invalid choice!")
    
    def reports_menu(self):
        """Reports and statistics menu"""
        while True:
            print("\n" + "="*60)
            print(" Reports and Statistics ".center(60, "-"))
            print("="*60)
            print("1. Course Statistics")
            print("2. Overall Statistics")
            print("3. Students by Course")
            print("4. Grade Distribution")
            print("5. Back to Main Menu")
            print("="*60)
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                course_id = input("Enter course ID: ").strip()
                avg, median = self.student_manager.get_statistics(course_id)
                if avg is not None:
                    print(f"\n{'='*60}")
                    print(f"Course: {course_id}")
                    print(f"Average Marks: {avg:.2f}")
                    print(f"Median Marks: {median:.2f}")
                    print(f"{'='*60}")
            
            elif choice == '2':
                avg, median = self.student_manager.get_statistics()
                if avg is not None:
                    print(f"\n{'='*60}")
                    print(f"Overall Statistics:")
                    print(f"Average Marks: {avg:.2f}")
                    print(f"Median Marks: {median:.2f}")
                    print(f"{'='*60}")
            
            elif choice == '3':
                course_id = input("Enter course ID: ").strip()
                students = [s for s in self.student_manager.students if s.course_id == course_id]
                if students:
                    print(f"\n{'='*80}")
                    print(f"Students in {course_id}: {len(students)}")
                    print(f"{'='*80}")
                    for student in students:
                        student.display_record()
                    print(f"{'='*80}")
                else:
                    print(f"No students found in {course_id}")
            
            elif choice == '4':
                print("\n--- Grade Distribution ---")
                course_id = input("Enter course ID (or press Enter for all): ").strip()
                
                students = self.student_manager.students
                if course_id:
                    students = [s for s in students if s.course_id == course_id]
                
                if not students:
                    print("No students found!")
                else:
                    # Count students in each grade
                    grade_counts = {}
                    for student in students:
                        grade = student.grade
                        grade_counts[grade] = grade_counts.get(grade, 0) + 1
                    
                    print(f"\n{'='*60}")
                    print(f"Total Students: {len(students)}")
                    print(f"{'='*60}")
                    for grade_obj in sorted(self.grade_manager.grades, key=lambda g: g.min_marks, reverse=True):
                        count = grade_counts.get(grade_obj.grade_letter, 0)
                        percentage = (count / len(students)) * 100 if students else 0
                        print(f"{grade_obj.grade_letter:5s} : {count:3d} students ({percentage:5.1f}%)")
                    print(f"{'='*60}")
            
            elif choice == '5':
                break
            else:
                print("Invalid choice!")


# MAIN ENTRY POINT

if __name__ == "__main__":
    app = CheckMyGradeApp()
# if not app.login_manager.users:
#     print("Creating default admin user...")
#     app.login_manager.register_user("micheal@mycsu.edu", "Welcome12#_", "professor")
    app.run()
    
        