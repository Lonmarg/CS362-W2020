from unittest import TestCase
import classroom_manager


def assertequal(self, thing1, thing2):
    if thing1 == thing2:
        return True
    else:
        self.fail()


def assertnotequal(self, thing1, thing2):
    if thing1 != thing2:
        return True
    else:
        self.fail()


class TestStudent(TestCase):
    def setUp(self):
        self.myId = 0
        self.first_name = "John"
        self.last_name = "Inglewild"
        self.student = classroom_manager.Student(self.myId, self.first_name, self.last_name)

    def test_get_full_name(self):
        self.setUp()

        assertequal(self, "John,Inglewild", self.student.get_full_name())

    def test_submit_assignment(self):
        self.setUp()

        assertequal(self, len(self.student.assignments), 0)

        self.name = "Assignment1"
        self.max_score = 10
        self.assignment = classroom_manager.Assignment(self.name, self.max_score)

        self.student.submit_assignment(self.assignment)
        assertequal(self, len(self.student.assignments), 1)
        assertequal(self, self.student.assignments[0].name, "Assignment1")

        self.name = "Assignment2"
        self.max_score = 15
        self.assignment = classroom_manager.Assignment(self.name, self.max_score)

        self.student.submit_assignment(self.assignment)
        assertequal(self, len(self.student.assignments), 2)
        assertequal(self, self.student.assignments[1].name, "Assignment2")

    def test_get_assignments(self):
        self.setUp()

        assertequal(self, len(self.student.assignments), 0)

        self.name = "Assignment"
        self.max_score = 10
        self.assignment = classroom_manager.Assignment(self.name, self.max_score)

        for x in range(1, 5):
            self.student.submit_assignment(self.assignment)

        assertequal(self, len(self.student.assignments), 4)

        returnedassignments = self.student.get_assignments()

        assertequal(self, len(returnedassignments), 4)

    def test_get_assignment(self):
        self.setUp()

        self.name = "Assignment1"
        self.max_score = 10
        self.assignment1 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment1)

        self.name = "Assignment2"
        self.max_score = 15
        self.assignment2 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment2)

        self.name = "Assignment3"
        self.max_score = 5
        self.assignment3 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment3)

        self.name = "Assignment4"
        self.max_score = 30
        self.assignment4 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment4)

        assertequal(self, self.student.get_assignment("Assignment1"), self.assignment1)
        assertequal(self, self.student.get_assignment("Assignment4"), self.assignment4)
        assertequal(self, self.student.get_assignment("Assignment2"), self.assignment2)
        assertnotequal(self, self.student.get_assignment("Assignment1"), self.assignment4)
        assertequal(self, self.student.get_assignment("Assignment6"), None)


    def test_get_average(self):
        self.setUp()

        assertequal(self, self.student.get_average(), 0)

        self.name = "Assignment1"
        self.max_score = 10
        self.assignment1 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment1)
        self.assignment1.assign_grade(5)

        assertequal(self, self.student.get_average(), 5)

        self.name = "Assignment2"
        self.max_score = 15
        self.assignment2 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment2)
        self.assignment2.assign_grade(10)

        assertequal(self, self.student.get_average(), 7.5)

        self.name = "Assignment3"
        self.max_score = 5
        self.assignment3 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment3)
        self.assignment3.assign_grade(3)

        assertequal(self, self.student.get_average(), 6)

        self.name = "Assignment4"
        self.max_score = 30
        self.assignment4 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment4)
        self.assignment4.assign_grade(12)

        assertequal(self, self.student.get_average(), 7.5)

    def test_remove_assignment(self):
        self.setUp()

        assertequal(self, len(self.student.get_assignments()), 0)

        self.student.remove_assignment("Assignment")
        assertequal(self, len(self.student.get_assignments()), 0)

        self.name = "Assignment1"
        self.max_score = 10
        self.assignment1 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment1)

        assertequal(self, len(self.student.get_assignments()), 1)
        assertequal(self, self.student.get_assignment("Assignment1"), self.assignment1)

        self.student.remove_assignment("Assignment1")
        assertequal(self, len(self.student.get_assignments()), 0)

        self.name = "Assignment1"
        self.max_score = 10
        self.assignment1 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment1)

        self.name = "Assignment2"
        self.max_score = 10
        self.assignment2 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment2)

        self.name = "Assignment3"
        self.max_score = 10
        self.assignment3 = classroom_manager.Assignment(self.name, self.max_score)
        self.student.submit_assignment(self.assignment3)

        assertequal(self, len(self.student.get_assignments()), 3)
        assertequal(self, self.student.get_assignment("Assignment1"), self.assignment1)

        self.student.remove_assignment("Assignment2")
        assertequal(self, len(self.student.get_assignments()), 2)
        assertequal(self, self.student.get_assignment("Assignment1"), self.assignment1)
        assertequal(self, self.student.get_assignment("Assignment2"), None)

class TestAssignment(TestCase):
    def setUp(self):
        self.name = "Assignment"
        self.max_score = 10

        self.assignment = classroom_manager.Assignment(self.name, self.max_score)

        assertequal(self, self.assignment.name, self.name)
        assertequal(self, self.assignment.max_score, self.max_score)
        assertequal(self, self.assignment.grade, -1)

    def test_assign_grade(self):
        self.setUp()

        self.assignment.assign_grade(5)
        assertequal(self, self.assignment.grade, 5)

        self.assignment.assign_grade(-7)
        assertequal(self, self.assignment.grade, -7)

        self.assignment.assign_grade(50)
        assertequal(self, self.assignment.grade, -1)

        self.assignment.assign_grade(0)
        assertequal(self, self.assignment.grade, 0)

        self.assignment.assign_grade(10)
        assertequal(self, self.assignment.grade, 10)

