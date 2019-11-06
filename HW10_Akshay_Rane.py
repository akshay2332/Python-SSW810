"""
Module 10 to maintain student repository of Universities
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
from utility import file_reading_gen


class Repository:
    """
    Repository class to hold data for every university
    """
    MAJOR_FIELDS = ("Dept", "Required", "Electives")

    def __init__(self, name, path, pretty_print):
        """
        Function to initiate the University Repository
        :param name: string specifying the name of university
        :param path: string specifying the directory to fetch university detail
        :param pretty_print: boolean specifying to print pretty tables
        """
        self.__name = name
        self._student_summary = defaultdict(Student)
        self._instructor_summary = defaultdict(Instructor)
        self._major_summary = defaultdict(map)

        if path is None:
            path = os.getcwd()

        self._populate_students(os.path.join(path, "students.txt"))
        self._populate_instructors(os.path.join(path, "instructors.txt"))
        self._populate_student_grades(os.path.join(path, "grades.txt"))
        self._populate_university_majors(os.path.join(path, "majors.txt"))

        if pretty_print:
            print(self._student_pretty_print())
            print(self._instructor_pretty_print())
            print(self._major_pretty_print())

    @property
    def get_repo_name(self):
        """
        Function to fetch the name of the repository
        """
        return self.__name

    def _add_student(self, student):
        """
        Function to add new student to the university
        """
        self._student_summary[student.get_cwid()] = student

    def fetch_students(self):
        """
        Function to fetch all the student in an university
        """
        return self._student_summary

    def _add_instructor(self, instructor):
        """
        Function to add an instructor to the university student_summary
        """
        self._instructor_summary[instructor.get_cwid()] = instructor

    def _populate_students(self, path):
        """
        Function to populate student data from students file
        :param path: where the file is located
        :return:
        """
        try:
            students_reader = file_reading_gen(path=path, fields=3,
                                               sep=';', header=True)

            for cwid, name, major in students_reader:
                student = Student(cwid, name, major)
                self._add_student(student)
        except FileNotFoundError as file_not_found:
            print(file_not_found)

        except ValueError as value_error:
            print(value_error)

    def _populate_instructors(self, path):
        """
        Function to populate instructors data from instructors file
        :param path: where the file is located
        :return:
        """
        try:
            instructors_reader = file_reading_gen(path=path, fields=3,
                                                  sep='|', header=True)

            for cwid, name, department in instructors_reader:
                instructor = Instructor(cwid, name, department)
                self._add_instructor(instructor)
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except ValueError as value_error:
            print(value_error)

    def _populate_student_grades(self, path):
        """
        Function to populate student grades from data file
        :param path: where the file is located
        :return:
        """

        try:
            grades_reader = file_reading_gen(path=path, fields=4,
                                             sep='|', header=True)

            for student_cwid, course_name, grade, instructor_cwid in grades_reader:
                if grade is None or ord(grade[0].upper()) - ord('A') > 2 or "C-" == grade:
                    continue

                if student_cwid in self._student_summary:
                    self._student_summary[student_cwid].add_course_grades(course_name, grade)
                else:
                    print(f"No student enrolled with cwid {student_cwid}")

                if instructor_cwid in self._instructor_summary:
                    self._instructor_summary[instructor_cwid].add_student(course_name)
                else:
                    print(f"No instructor found with cwid {instructor_cwid}")

        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except ValueError as value_error:
            print(value_error)

    def _populate_university_majors(self, path):
        """
        Function to populate university major details
        :param path: where the file is located
        :return:
        """

        try:
            majors_reader = file_reading_gen(path=path, fields=3,
                                             sep='\t', header=True)

            for major, status_flag, course_name in majors_reader:
                if major in self._major_summary:

                    if status_flag in self._major_summary[major]:
                        self._major_summary[major][status_flag].add(course_name)
                    else:
                        self._major_summary[major][status_flag] = {course_name}
                else:
                    self._major_summary[major] = {status_flag: {course_name}}

        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except ValueError as value_error:
            print(value_error)

    def fetch_instructors(self):
        """
        Function to fetch all the information of instructors in an university
        """
        return self._instructor_summary

    def fetch_majors(self):
        """
        Function to fetch all the information of majors in an university
        """
        return self._major_summary

    def fetch_major_details(self):
        """
        Function to fetch details for majors
        :return: major name, required courses, elective courses
        """
        for major, major_info in self._major_summary.items():
            yield [major, list(major_info["R"]), list(major_info["E"])]

    def _student_pretty_print(self):
        """
        Function to print the summary of students in an university
        """

        pretty_table = PrettyTable()
        pretty_table.field_names = list(Student.STUDENT_FIELDS)

        for student_info in self._student_summary.values():
            student_details = student_info.fetch_student_details()
            course_catalog = self._major_summary[student_info.get_major()]

            student_courses = set(student_info.courses_taken())

            required_remaining = course_catalog["R"] - student_courses
            electives_remaining = course_catalog["E"] - student_courses

            student_details.append(required_remaining)
            if len(electives_remaining) < len(course_catalog["E"]):
                student_details.append(None)
            else:
                student_details.append(electives_remaining)

            pretty_table.add_row(student_details)

        return pretty_table

    def _instructor_pretty_print(self):
        """
        Function to print the summary of instructors in an university
        """

        pretty_table = PrettyTable()
        pretty_table.field_names = list(Instructor.INSTRUCTORS_FIELDS)

        for instructor_info in self._instructor_summary.values():
            for row in instructor_info.fetch_instructor_details():
                pretty_table.add_row(row)

        return pretty_table

    def _major_pretty_print(self):
        """
        Function to print the summary of majors in an university
        """

        pretty_table = PrettyTable()
        pretty_table.field_names = list(Repository.MAJOR_FIELDS)
        for row in self.fetch_major_details():
            pretty_table.add_row(row)

        return pretty_table


class Student:
    """
    Class to maintain student details cwid, name, major
    """
    STUDENT_FIELDS = ("CWID", "Name", "Completed Courses", "Remaining Required", "Remaining Electives")

    def __init__(self, cwid, name, major):
        """
        :param cwid: unique for all students
        :param name: string specifying the name
        :param major: string specifying the major
        """
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = defaultdict(str)

    def get_cwid(self):
        """
        Function to fetch the student objects cwid
        :return: string cwid
        """
        return self._cwid

    def get_name(self):
        """
        Function to fetch the student objects name
        :return: string name
        """
        return self._name

    def get_major(self):
        """
        Function to fetch the student objects major
        :return: string major
        """
        return self._major

    def get_course_grade(self):
        """
        Function to fetch the student objects courses
        :return: string major
        """
        return self._courses

    def add_course(self, course_name):
        """
        Function To add a course for the student
        """
        self._courses[course_name] = None

    def add_course_grades(self, course_name, grade):
        """
        Function to add grades to the course
        """
        self._courses[course_name] = grade

    def change_major(self, major):
        """
        Function to change major for a student
        """
        self._major = major

    def courses_taken(self):
        """
        Function to fetch the courses taken by a student
        :return:
        """
        return list(self._courses.keys())

    def fetch_student_details(self):
        """
        Function to fetch student details
        :return: list of student instance variables
        """

        return [self._cwid, self._name, sorted(self.courses_taken())]

    def __str__(self):
        """
        Function to stringify the student class
        """
        return f"cwid | {self._cwid} | name | {self._name} | major | {self._major}"


class Instructor:
    """
    Instructor class to store information og instructors in universities
    """
    INSTRUCTORS_FIELDS = ("CWID", "Name", "Dept", "Course", "Students")

    def __init__(self, cwid, name, department):
        """
        :param cwid: uniquie Id for an instructor
        :param name: string specifying the name of an instructor
        :param department: string specifying the department the instructor belong to
        """
        self._cwid = cwid
        self._name = name
        self._department = department
        self._courses_student_count = defaultdict(int)

    def get_cwid(self):
        """
        Function to fetch the Instructor objects cwid
        :return: string cwid
        """
        return self._cwid

    def get_name(self):
        """
        Function to fetch the Instructor objects name
        :return: string name
        """
        return self._name

    def get_department(self):
        """
        Function to fetch the Instructor objects department
        :return: string department
        """
        return self._department

    def add_student(self, course_name):
        """
        Function to add student to the instructors course
        """
        self._courses_student_count[course_name] += 1

    def change_department(self, department):
        """
        Function to change the department of an instructors
        """
        self._department = department

    def courses_taught(self):
        """
        Function to return the courses taught by instructors
        :return: list of courses
        """
        return list(self._courses_student_count.keys())

    def course_enrollments(self, course_name):
        """
        Function to return the number of enrollments in the course
        :param course_name: the course whose enrollment needs to find
        :return: int representing the course enrollment
        """
        return self._courses_student_count[course_name] \
            if course_name in self._courses_student_count else 0

    def fetch_instructor_details(self):
        """
        Fucntion to fetch instructor details
        :return: list of instance variable
        """
        for course_name, student_count in self._courses_student_count.items():
            yield [self._cwid, self._name, self._department, course_name, student_count]

    def __str__(self):
        """
        Function to stringify the instructor details
        """
        return f"cwid | {self._cwid} | name | {self._name} | department | {self._department}"


if __name__ == "__main__":
    stevens_repository = Repository("Stevens", None, True)
