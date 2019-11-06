"""
Test module for Homework-09 to verify instructors and student details.
"""
import unittest
from HW10_Akshay_Rane import Repository


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

        self.assertEqual(student_summary["10172"].courses_taken(), ["SSW 555", "SSW 567"])
        self.assertEqual(student_summary["10183"].courses_taken(), ["SSW 689"])
        self.assertNotEqual(student_summary["11399"].courses_taken(), ["SSW 689"])

    def test_instructor_summary(self):
        """
        Test function to test the summary of instructors in a repository
        """
        repository = Repository("STEVENS", None, False)
        instructor_summary = repository.fetch_instructors()

        self.assertEqual(instructor_summary["98765"].course_enrollments("SSW 567"), 4)
        self.assertEqual(instructor_summary["98764"].course_enrollments("SSW 687"), 3)
        self.assertEqual(instructor_summary["98763"].course_enrollments("SSW 555"), 1)

    def test_major_summary(self):
        """
        Test function to test the summary of majors in a university repository
        """

        repository = Repository("STEVENS", None, False)
        major_summary = repository.fetch_majors()

        self.assertEqual(major_summary["SFEN"]["R"], set(['SSW 564', 'SSW 540', 'SSW 555', 'SSW 567']))
        self.assertEqual(major_summary["SFEN"]["E"], set(['CS 513', 'CS 501', 'CS 545']))
        self.assertEqual(major_summary["SYEN"]["R"], set(['SYS 612', 'SYS 671', 'SYS 800']))
        self.assertEqual(major_summary["SYEN"]["E"], set(['SSW 565', 'SSW 540', 'SSW 810']))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
