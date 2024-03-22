"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the Graph and Course Classes for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from __future__ import annotations


class _Course:
    """
    A course in a graph (acts as a vertex).

    Instance Attributes:
    - code: the course code (ex. CSC111)
    - prerequisites: the courses that point to this course
    - dependents: the courses that this course points to

    Representation Invariants:
    """
    code: str
    prerequisites: list[set]
    dependents: set[_Course]

    # extra / implement later
    name: str
    description: str
    breadth: int
    credit: float
    exclusions: set[_Course]
    corequisites: set[_Course]

    def __init__(self, code: str) -> None:
        """Initialize a new course vertex with the given code, prerequisites, and dependents."""
        self.code = code
        self.prerequisites = []
        self.dependents = set()
        if code[6] == 'Y':
            self.credit = 1.0
        else:
            self.credit = 0.5


class Graph:
    """
    A graph. Each vertice of the graph is a course.

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
        """
        Add a course to this graph.
        The new course is not adjacent to any other vertices.
        """
        if course_code not in self._courses:
            self._courses[course_code] = _Course(course_code)

    def add_prerequisites(self, prereq: set, course: str) -> None:
        """Updates a courses prerequisites. This funcitons takes in a set of related courses or "options"
        to meet a prerequisite requirement. The function will add one of these courses to all the current sets
        to create a list containing sets of all the different courses.
        If a tuple is taken in, all elements need to be taken together.
        """
        if (all({p in self._courses if isinstance(p, str) else all(p1 in self._courses for p1 in p) for p in prereq})
                and course in self._courses):
            course_v = self._courses[course]
            if course_v.prerequisites != []:
                combine_lists(course_v.prerequisites, prereq)
            else:
                for courses in prereq:
                    if isinstance(courses, str):
                        course_v.prerequisites.append({courses})
                    else:
                        course_v.prerequisites.append(set(courses))
        else:
            raise ValueError

    def add_dependents(self, course: str, dependent: str) -> None:
        """Add a dependant to a given course
        >>> g = Graph()
        >>> g.add_course('MAT135H1')
        >>> g.add_course('MAT136H1')
        >>> g.add_dependents('MAT135H1', 'MAT136H1')
        >>> {c.code for c in g._courses['MAT135H1'].dependents}
        {'MAT136H1'}
        """
        if course in self._courses and dependent in self._courses:
            course_v = self._courses[course]
            dependent_v = self._courses[dependent]
            course_v.dependents.add(dependent_v)
        else:
            raise ValueError

    def get_prerequisites(self, course_code: str) -> list:
        """Returns a list of courses that are prerequisites to the given course
        """
        if self._courses[course_code].prerequisites == []:
            return []
        else:
            all_prereq = []
            for course_set in self._courses[course_code].prerequisites:
                new_prereq = []
                for course in course_set:
                    course_prereq = self.get_prerequisites(course).copy()
                    combine_lists(course_prereq, {course})
                    combine_lists2(new_prereq, course_prereq)
                all_prereq += new_prereq
            return all_prereq

    def get_dependents(self, course_code: str) -> set:
        """Returns a list of courses that are dependents to the given course
        ***DECIDE IF IT SHOULD RETURN A LIST OF _COURSE OR STR (COURSE_CODE)***
        """
        return {course.code for course in self._courses[course_code].dependents}


def combine_lists(lst1: list[set], set2: set) -> None:
    """Mutate list 1 such that each set in lst1 has exactly one elemnt of set2
    for as many times as sets in lst2. Special mutation to account for posisble tuples in set2.
    >>> lst1 = [{1, 2, 3}, {4}]
    >>> combine_lists(lst1,{5, 6} )
    >>> len(lst1)
    4
    >>> lst1 = []
    >>> combine_lists(lst1,{5, 6} )
    >>> lst1
    [{5}, {6}]
    """
    if lst1 == []:
        for set_element in set2:
            lst1.append({set_element})
    else:
        new_lst = lst1[:]
        for set_element in set2:
            for list_element in new_lst:
                if isinstance(set_element, tuple):
                    lst1.append(list_element.union(set(set_element)))
                else:
                    lst1.append(list_element.union({set_element}))
        for element in new_lst:
            lst1.remove(element)


def combine_lists2(lst1: list[set], lst2: list[set]) -> None:
    """Mutate list 1 such that each set in lst1 has exactly one elemnt of list2
    for as many times as sets in lst2. Lst2 only has sets that have no tuples.
    >>> lst1 = [{1, 2, 3}, {4}]
    >>> combine_lists2(lst1, [{5, 6}, {7, 8}])
    >>> len(lst1)
    4
    >>> lst1 = []
    >>> combine_lists2(lst1, [{5, 6}, {7, 8}])
    >>> lst1 == [{5, 6}, {7, 8}]
    True
    >>> lst1 = [{1, 2, 3}, {4}]
    >>> combine_lists2(lst1, [{5}])
    >>> len(lst1)
    2
    """
    if lst1 == []:
        for set_element in lst2:
            lst1.append(set_element)
    else:
        new_lst = lst1[:]
        for element in lst2:
            for list_element in new_lst:
                lst1.append(list_element.union(element))
        for element in new_lst:
            lst1.remove(element)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
