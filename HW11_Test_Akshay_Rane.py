"""
Test module for Homework-11 to verify instructors and student details.
"""
import unittest
import sqlite3
from HW11_Akshay_Rane import Repository


class TestModuleRepository(unittest.TestCase):
    """
    Test Class to test the function of repository module
    """

    def test_student_summary(self):
        """
        Test function to test the summary of students in a repository
        """
        repository = Repository("STEVENS", None, False)

        student_summary = repository.fetch_students()

        self.assertEqual(student_summary["10103"].courses_taken(), ["SSW 810", "CS 501"])
        self.assertEqual(student_summary["10115"].courses_taken(), ["SSW 810"])
        self.assertEqual(student_summary["10183"].courses_taken(), ["SSW 555", "SSW 810"])
        self.assertEqual(student_summary["11714"].courses_taken(), ["SSW 810", "CS 546", "CS 570"])

    def test_instructor_summary(self):
        """
        Test function to test the summary of instructors in a repository
        """
        repository = Repository("STEVENS", None, False)
        instructor_summary = repository.fetch_instructors()

        self.assertEqual(instructor_summary["98762"].course_enrollments("CS 501"), 1)
        self.assertEqual(instructor_summary["98764"].course_enrollments("CS 546"), 1)
        self.assertEqual(instructor_summary["98763"].course_enrollments("SSW 810"), 4)

    def test_major_summary(self):
        """
        Test function to test the summary of majors in a repository
        """

        repository = Repository("STEVENS", None, False)
        major_summary = repository.fetch_majors()

        self.assertEqual(major_summary["SFEN"]["R"], set(['SSW 540', 'SSW 555', 'SSW 810']))
        self.assertEqual(major_summary["SFEN"]["E"], set(['CS 501', 'CS 546']))
        self.assertEqual(major_summary["CS"]["R"], set(['CS 546', 'CS 570']))
        self.assertEqual(major_summary["CS"]["E"], set(['SSW 565', 'SSW 810']))

    def test_instructor_table_db(self):
        """
        Test function to test database retrieve function
        :return:
        """

        try:
            db_connection = sqlite3.connect("810_startup.db")
        except sqlite3.OperationalError as error:
            print(f"ERROR: Not able to open the database 810_startup.db.")
        else:
            query = """SELECT gd.InstructorCWID as CWID,inst.Name, inst.Dept,
                        gd.Course,count(gd.StudentCWID)
                        as Students from grades as gd join instructors as inst on
                        gd.InstructorCWID =
                        inst.CWID group by gd.InstructorCWID, gd.Course"""

            db_dictionary = {}

            for row in db_connection.execute(query):
                db_dictionary[row[3]] = row[4]

            db_connection.close()

        self.assertEqual(db_dictionary["CS 570"], 1)
        self.assertEqual(db_dictionary["CS 546"], 1)
        self.assertEqual(db_dictionary["SSW 810"], 4)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
