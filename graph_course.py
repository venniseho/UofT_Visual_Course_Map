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
    prerequisites: set[_Course]
    dependents: set[_Course]

    # extra / implement later
    name: str
    description: str
    breadth: int
    exclusions: set[_Course]
    corequisites: set[_Course]

    def __init__(self, code: str, prerequisites: set[_Course], dependents: set[_Course]) -> None:
        """Initialize a new course vertex with the given code, prerequisites, and dependents."""
        self.code = code
        self.prerequisites = prerequisites
        self.dependents = dependents


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
            self._courses[course_code] = _Course(course_code, set(), set())

    def add_prerequisites(self):
        """Similar to add_edge from class"""
        # TODO

    def add_dependents(self):
        """Similar to add_edge from class"""
        # TODO

    def get_prerequisites(self, course_code) -> list[_Course, str]:
        """Returns a list of courses that are prerequisites to the given course
        ***DECIDE IF IT SHOULD RETURN A LIST OF _COURSE OR STR (COURSE_CODE)***
        """
        # TODO

    def get_dependents(self, course_code) -> list[_Course, str]:
        """Returns a list of courses that are dependents to the given course
        ***DECIDE IF IT SHOULD RETURN A LIST OF _COURSE OR STR (COURSE_CODE)***
        """
        # TODO


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['annotations'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
