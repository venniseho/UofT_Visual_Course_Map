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


class Expr:
    """A general expression in our abstract syntax tree
    """

    def __init__(self) -> None:
        pass

    def evaluate(self) -> Any:
        """Evaluates an expression, whetehr it;s a course or a BoolOp
        """
        raise NotImplementedError


class _Course(Expr):
    """A course in a graph (acts as a vertex).

    Instance Attributes:
    - code: the course code (ex. CSC111)
    - prerequisites: the courses that point to this course
    - dependents: the courses that this course points to

    Representation Invariants:
    """
    code: str
    prerequisites: BoolOp
    dependents: set[_Course]

    # extra / implement later
    name: str
    description: str
    breadth: int
    credit: float
    exclusions: set[_Course]
    corequisites: set[_Course]

    def __init__(self, code: str) -> None:
        """Initialize a new course vertex with the given code, prerequisites, and dependents.
        """
        super().__init__()
        self.code = code
        self.prerequisites = BoolOp('and', [])
        self.dependents = set()
        self.credit = 1.0 if code[6] == 'Y' else 0.5
        self.exclusions = set()
        self.corequisites = set()

    def evaluate(self) -> list:
        """Evaluate the course to give itself and its prerequisites
        """
        return combine_lists3([{self.code}], self.prerequisites.evaluate())

    def are_exclusions(self, course: _Course) -> bool:
        """Check if self and course are exclusions of each other"""
        return course in self.exclusions and self in course.exclusions


class Graph:
    """A graph. Each vertice of the graph is a course.

    Representation Invariants:
    """
    # Private Instance Attributes:
    #   - _courses:
    #       A collection of the courses contained in this graph.
    #       Maps course code to _Course object.
    _courses: dict[str, _Course]

    def __init__(self) -> None:
        self._courses = {}

    def add_course(self, course_code: str) -> None:
        """Add a course to this graph.
        The new course is not adjacent to any other vertices.
        """
        if course_code not in self._courses:
            self._courses[course_code] = _Course(course_code)

    def add_exclusion(self, course_code: str, exclusion: set[str]) -> None:
        """Add an exclusion to course code
        """
        if course_code in self._courses and all(exc in self._courses for exc in exclusion):
            for ex in exclusion:
                self._courses[course_code].exclusions.add(self._courses[ex])
        else:
            raise ValueError

    def add_corequisites(self, course_code: str, coreq: set[str]) -> None:
        """Add an exclusion to course code
        """
        if course_code in self._courses and all(cor in self._courses for cor in coreq):
            for co in coreq:
                self._courses[course_code].corequisites.add(self._courses[co])
        else:
            raise ValueError

    def add_prerequisites2(self, prereq: set, course: str) -> None:
        """Updates a courses prerequisites. This funcitons takes in a set of related courses or "options"
        to meet a prerequisite requirement. The function will add one of these courses to all the current sets
        to create a list containing sets of all the different coursecombos needed to meet the prereq for that course.
        If a tuple is taken in, all elements need to be taken together.
        """
        if (all({p in self._courses if isinstance(p, str) else all(p1 in self._courses for p1 in p) for p in prereq})
                and course in self._courses):
            course_v = self._courses[course]
            prereq_v = [BoolOp('and', [self._courses[code] for code in course_code])
                        if isinstance(course_code, tuple)
                        else self._courses[course_code] for course_code in prereq]
            course_v.prerequisites.operand.append(BoolOp('or', prereq_v))
        else:
            raise ValueError

    def add_dependents(self, course: str, dependent: str) -> None:
        """Add a dependant to a given course
        """
        if course in self._courses and dependent in self._courses:
            course_v = self._courses[course]
            dependent_v = self._courses[dependent]
            course_v.dependents.add(dependent_v)
        else:
            raise ValueError

    def get_all_prerequisites(self, course_code: str) -> list:
        """Returns a list of courses that are prerequisites to the given course in str form
        """
        prereqs = self._courses[course_code].prerequisites.evaluate()
        for prereq_set in prereqs:
            coreq = set()
            for prereq in prereq_set:
                coreqs = {co.code for co in self._courses[prereq].corequisites}
                coreq.update(coreqs)
            prereq_set.update(coreq)

        return [set_prereq for set_prereq in prereqs if not any(
            self._courses[pre].are_exclusions(self._courses[exclusion]) for pre in set_prereq for exclusion in
            set_prereq)]

    def get_prerequisites(self, course_code: str, completed: set[str], exclude: set[str], credit: float) -> list:
        """Returns the pathways under the specified number of credits to meet the prerequisite for a given course
        given a set of courses the user has already completed and a set of courses the user wants to avoid.
        In the case of a tie, return all possibilities.
        """
        prereqs = self.get_all_prerequisites(course_code)
        new_prereqs = [prereq_set for prereq_set in prereqs if not any(prereq in exclude for prereq in prereq_set)]
        not_completed = [{prereq for prereq in prereq_set if prereq not in completed} for prereq_set in new_prereqs]
        all_exclusions = {course_ex.code for completed_course in completed for course_ex in
                          self._courses[completed_course].exclusions}
        excluded = [prereq_set for prereq_set in not_completed if
                    not any(prereq in all_exclusions for prereq in prereq_set)]
        return [pathway for pathway in sorted([(count_credits(course_set), course_set) for course_set in excluded]) if
                pathway[0] <= credit]

    def get_dependents(self, course_code: str) -> set:
        """Returns a list of courses that are dependents to the given course
        ***DECIDE IF IT SHOULD RETURN A LIST OF _COURSE OR STR (COURSE_CODE)***
        """
        return {course.code for course in self._courses[course_code].dependents}


class BoolOp(Expr):
    """and/or class
    """
    op: str
    operand: list[Expr]

    def __init__(self, operator: str, operands: list[Expr]) -> None:
        super().__init__()
        self.op = operator
        self.operand = operands

    def evaluate(self) -> list:
        """This function returns a list of sets of different possibilities to meet an outcome. For example, if we have
        the BoolOp tree 'and' with operands A, B, and BoolOp('or', [C, D]), then we get
        [{A, B, C}, {A, B, D}]
        """
        if not self.operand:
            return []
        else:
            if self.op == 'and':
                new_list = []
                for operand in self.operand:
                    new_list = combine_lists3(new_list, [operand.evaluate()]) \
                        if isinstance(operand.evaluate(), set) \
                        else combine_lists3(new_list, operand.evaluate())
            else:
                new_list = []
                for operand in self.operand:
                    new_list = new_list + operand.evaluate() \
                        if isinstance(operand.evaluate(), list) \
                        else new_list + [operand.evaluate()]
            return new_list


def combine_lists3(lst1: list[set], lst2: list[set]) -> list:
    """Mutate list 1 such that each set in lst1 has exactly one elemnt of list2
    for as many times as sets in lst2. Lst2 only has sets that have no tuples.
    Preconditions:
        - lst1 != [] or lst2 != []
    """
    if not lst1:
        return lst2
    elif not lst2:
        return lst1
    else:
        return [element1.union(element2) for element1 in lst1 for element2 in lst2]


def count_credits(course_set: set[str]) -> int:
    """Count the number of credits in a set of strings\
    """
    return sum([1.0 if course[6] == 'Y' else 0.5 for course in course_set])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
