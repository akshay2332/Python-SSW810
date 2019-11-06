"""
Test module for Homework-09 to verify instructors and student details.
"""
import unittest
from HW09_Akshay_Rane import Repository


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


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
