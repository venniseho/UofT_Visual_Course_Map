"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the Graph and Course Classes for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from __future__ import annotations
from typing import Any
from expression_tree_classes import _Course, Tree, BoolOp


class Graph:
    """A graph. Each vertice of the graph is a course.

    Representation Invariants:
        - all(len(course) == 8 for course in self._courses)
        - all(course[6:8] == 'H1' or course[6:8] == 'Y1' for course in self._courses)
    """
    # Private Instance Attributes:
    #   - _courses:
    #       A collection of the courses contained in this graph.
    #       Maps course code to _Course object.

    _courses: dict[str, _Course]

    def __init__(self) -> None:
        self._courses = {}

    def valid_course(self, course: str) -> bool:
        """Returns True if course in self._courses.
        """
        if course in self._courses:
            return True
        return False

    def add_course(self, course_code: str) -> None:
        """Add a course to this graph.
        The new course is not adjacent to any other vertices.
        Preconditions:
            - len(course_code) == 8
            - course_code[6:8] == 'H1' or course_code[6:8] == 'Y1'
        """
        if course_code not in self._courses:
            self._courses[course_code] = _Course(course_code)

    def add_exclusion(self, course_code: str, exclusion: set[str]) -> None:
        """Add an exclusion to course code
        Preconditions:
            - len(course_code) == 8
            - course_code[6:8] == 'H1' or course_code[6:8] == 'Y1'
            - all(ex in self._courses for ex in exclusion)
        """
        if course_code in self._courses:
            for ex in exclusion:
                if ex in self._courses:
                    self._courses[course_code].exclusions.add(self._courses[ex])
        else:
            raise ValueError

    def add_prerequisites(self, prereq: list, course: str) -> None:
        """Updates a courses prerequisites. This funcitons takes in a set of related courses or "options"
        to meet a prerequisite requirement. The function will add one of these courses to all the current sets
        to create a list containing sets of all the different coursecombos needed to meet the prereq for that course.
        If a tuple is taken in, all elements need to be taken together.
        Preconditions:
            - len(course_code) == 8
            - course_code[6:8] == 'H1' or course_code[6:8] == 'Y1'
        """
        if course in self._courses:
            course_v = self._courses[course]
            course_v.prerequisites.operand.append(self.create_boolop(prereq))
        else:
            raise ValueError

    def tuple_to_bool(self, tup: tuple) -> BoolOp:
        """Takes in a tuple of tuples and turns it into a BoolOp"""
        bool_so_far = BoolOp('and', [])
        for course_code in tup:
            if isinstance(course_code, tuple):
                temp_bool = BoolOp('or', [])
                for code in course_code:
                    temp_bool.operand.append(self._courses[code])
                bool_so_far.operand.append(temp_bool)
            else:
                bool_so_far.operand.append(self._courses[course_code])
        return bool_so_far

    def get_all_prerequisites(self, course_code: str) -> list:
        """Returns a list of courses that are prerequisites to the given course in str form
        Preconditions:
            - len(course_code) == 8
            - course_code[6:8] == 'H1' or course_code[6:8] == 'Y1'
        """
        prereqs = self._courses[course_code].prerequisites.evaluate()
        prereq_exclusions = [set_prereq for set_prereq in prereqs if not any(
            self._courses[pre].are_exclusions(self._courses[exclusion]) for pre in set_prereq for exclusion in
            set_prereq)]

        for ex_prereqs in prereq_exclusions.copy():
            if any(ex_prereq_pathway.issubset(ex_prereqs) and ex_prereq_pathway != ex_prereqs for ex_prereq_pathway in
                   prereq_exclusions.copy()):
                prereq_exclusions.remove(ex_prereqs)

        return prereq_exclusions

    def get_prerequisites(self, course_code: str, completed: set[str], exclude: set[str], credit: float) -> list:
        """Returns the pathways under the specified number of credits to meet the prerequisite for a given course
        given a set of courses the user has already completed and a set of courses the user wants to avoid.
        In the case of a tie, return all possibilities.
        Preconditions:
            - len(course_code) == 8
            - course_code[6:8] == 'H1' or course_code[6:8] == 'Y1'
            - all(ex in self._courses for ex in exclusion)
            - all(code in self._courses for code in completed)
        """
        prereqs = self.get_all_prerequisites(course_code)
        new_prereqs = [prereq_set for prereq_set in prereqs if not any(prereq in exclude for prereq in prereq_set)]
        not_completed = [{prereq for prereq in prereq_set if prereq not in completed} for prereq_set in new_prereqs]
        all_exclusions = {course_ex.code for completed_course in completed for course_ex in
                          self._courses[completed_course].exclusions}
        excluded = [prereq_set for prereq_set in not_completed if
                    not any(prereq in all_exclusions for prereq in prereq_set)]

        for with_excluded in excluded.copy():
            if any(excluded_pathway.issubset(with_excluded) and excluded_pathway != with_excluded for excluded_pathway
                   in excluded.copy()):
                excluded.remove(with_excluded)

        return [pathway for pathway in sorted([(count_credits(course_set), course_set) for course_set in excluded]) if
                pathway[0] <= credit]

    def course_to_tree(self, course_code: str) -> Tree:
        """Returns a tree of prerequisites based on the course code
        Preconditions:
            - len(course_code) == 8
            - course_code[6:8] == 'H1' or course_code[6:8] == 'Y1'
        """
        return self._courses[course_code].to_tree()

    def create_boolop(self, courses: Any) -> BoolOp:
        """Takes in a list/tuple of courses with tuples and lists and returns a corresponding BoolOp"""
        if isinstance(courses, tuple):
            bool_so_far = BoolOp('and', [])
        else:
            bool_so_far = BoolOp('or', [])
        for course_code in courses:
            if isinstance(course_code, str):
                bool_so_far.operand.append(self._courses[course_code])
            else:
                bool_so_far.operand.append(self.create_boolop(course_code))
        return bool_so_far


def count_credits(course_set: set[str]) -> int:
    """Count the number of credits in a set of strings
    Preconditions:
        - all(len(course) == 8 for course in course_set)
        - all(course[6:8] == 'H1' or course[6:8] == 'Y1' for course in course_set)
    """
    return sum([1.0 if course[6] == 'Y' else 0.5 for course in course_set])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations', '_Course', 'Tree', 'BoolOp', 'expression_tree_classes'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
