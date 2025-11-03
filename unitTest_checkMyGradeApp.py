import unittest
import os
import time

from CheckMyGrade_lab_work_1 import (
    StudentManager,
    CourseManager,
    ProfessorManager,
    Student,
    Course,
    Professor,
)

class TestCheckMyGrade(unittest.TestCase):

    def setUp(self):
        # using temp csv names so I don't overwrite real data
        self.student_mgr = StudentManager(csv_file='test_students.csv')
        self.course_mgr = CourseManager(csv_file='test_courses.csv')
        self.prof_mgr = ProfessorManager(csv_file='test_professors.csv')

        self.student_mgr.students = []
        self.student_mgr.save_to_csv()

    #STUDENTS CRUD tests    

    def test_add_student(self):
        s = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 95)
        added = self.student_mgr.add_student(s)
        self.assertTrue(added)
        self.assertEqual(len(self.student_mgr.students), 1)

    def test_update_student(self):
        s = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 95)
        self.student_mgr.add_student(s)
        self.student_mgr.update_student("sam@mycsu.edu", first_name="Samuel")
        self.assertEqual(self.student_mgr.students[0].first_name, "Samuel")

    def test_delete_student(self):
        s = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 95)
        self.student_mgr.add_student(s)
        self.student_mgr.delete_student("sam@mycsu.edu")
        self.assertEqual(len(self.student_mgr.students), 0)

    def test_sort_students_by_marks(self):
        # adding few more
        self.student_mgr.add_student(Student("a@x.com", "A", "A", "DATA200", "B", 80))
        self.student_mgr.add_student(Student("b@x.com", "B", "B", "DATA200", "A", 95))
        elapsed = self.student_mgr.sort_students(by='marks', ascending=False)
        # highest marks first
        self.assertEqual(self.student_mgr.students[0].marks, 95)
        # printing time 
        print("Sort time:", elapsed)

    # Performance of 1000 Records
    def test_search_time_on_big_file(self):
        """
        As per the doc: load data from previous runs (csv) and print total time in search cases.
        """
        if not os.path.exists('students.csv'):
            self.skipTest("students.csv with 1000 records not found")

        big_mgr = StudentManager(csv_file='students.csv')
        start = time.time()
        # try to find one that likely exists from the generator
        big_mgr.search_student("student500@mycsu.edu")
        end = time.time()
        print(f"Search time on 1000 records: {end - start:.6f} seconds")

    # COURSE TESTS 

    def test_add_course(self):
        c = Course("DATA200", "Data 200", "Test course")
        added = self.course_mgr.add_course(c)
        self.assertTrue(added)

    def test_delete_course(self):
        c = Course("DATA201", "Data 201", "Another course")
        self.course_mgr.add_course(c)
        deleted = self.course_mgr.delete_course("DATA201")
        self.assertTrue(deleted)

    # PROFESSOR TESTS 

    def test_add_professor(self):
        p = Professor("p1@mycsu.edu", "Dr. Smith", "Assistant", "DATA200")
        added = self.prof_mgr.add_professor(p)
        self.assertTrue(added)

    def test_delete_professor(self):
        p = Professor("p2@mycsu.edu", "Dr. Wayne", "Associate", "DATA201")
        self.prof_mgr.add_professor(p)
        deleted = self.prof_mgr.delete_professor("p2@mycsu.edu")
        self.assertTrue(deleted)


if __name__ == '__main__':
    unittest.main()