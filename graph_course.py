"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the Graph and Course Classes for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from __future__ import annotations
from expression_tree_classes import _Course, Tree, BoolOp


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
        if course_code in self._courses:
            for ex in exclusion:
                if ex in self._courses:
                    self._courses[course_code].exclusions.add(self._courses[ex])
        else:
            raise ValueError

    def add_corequisites(self, course_code: str, coreq: set[str]) -> None:
        """Add an exclusion to course code
        """
        if course_code in self._courses:
            for co in coreq:
                if co in self._courses:
                    self._courses[course_code].corequisites.add(self._courses[co])
        else:
            raise ValueError


    def add_prerequisites(self, prereq: list, course: str) -> None:
        """
        Updates a courses prerequisites. This funcitons takes in a set of related courses or "options"
        to meet a prerequisite requirement. The function will add one of these courses to all the current sets
        to create a list containing sets of all the different coursecombos needed to meet the prereq for that course.
        If a tuple is taken in, all elements need to be taken together.
        """
        # checks if the course exists as a vertice in the graph
        if course in self._courses:
            course_v = self._courses[course]
            prereq_v = []
            for course_code in prereq:
                if isinstance(course_code, tuple):
                    prereq_v.append(self.tuple_to_bool(course_code))
                else:
                    if course_code in self._courses:
                        prereq_v.append(self._courses[course_code])
            course_v.prerequisites.operand.append(BoolOp('or', prereq_v))
        else:
            raise ValueError

    def tuple_to_bool(self, tup: tuple) -> BoolOp:
        """Takes in a tuple of tuples and turns it into a BoolOp"""
        bool_so_far = BoolOp('and', [])
        for course_code in tup:
            if isinstance(course_code, list):
                temp_bool = BoolOp('or', [])
                for code in course_code:
                    temp_bool.operand.append(self._courses[code])
                bool_so_far.operand.append(temp_bool)
            else:
                bool_so_far.operand.append(self._courses[course_code])
        return bool_so_far

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
        # for prereq_set in prereqs:
        #     coreq = set()
        #     for prereq in prereq_set:
        #         coreqs = {co.code for co in self._courses[prereq].corequisites}
        #         coreq.update(coreqs)
        #     prereq_set.update(coreq)

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
           >>> g = Graph()
   >>> for course in {'MAT135H1','MAT136H1', 'MAT137Y1', 'MAT157Y1', 'MAT223H1', 'MAT240H1', 'MAT237Y1', 'MAT235Y1', 'MAT138H1'}:
   ...     g.add_course(course)
   >>> for course in {'CSC413H1', 'CSC108H1', 'CSC148H1', 'CSC110Y1', 'CSC111H1', 'STA237H1'}:
   ...     g.add_course(course)
   >>> g.add_prerequisites({('MAT135H1', 'MAT136H1', 'MAT138H1'), 'MAT137Y1', 'MAT157Y1'}, 'MAT237Y1')
   >>> g.add_prerequisites({('MAT135H1', 'MAT136H1'), 'MAT137Y1', 'MAT157Y1'}, 'MAT235Y1')
   >>> g.add_prerequisites({'MAT237Y1', 'MAT235Y1'}, 'CSC413H1')
   >>> g.add_prerequisites({'CSC148H1', 'CSC111H1'}, 'CSC413H1')
   >>> g.add_prerequisites({'STA237H1'}, 'CSC413H1')
   >>> g.add_prerequisites({'CSC108H1'}, 'CSC148H1')
   >>> g.add_prerequisites({'CSC110Y1'}, 'CSC111H1')
   >>> g.add_prerequisites({'MAT223H1', 'MAT240H1'}, 'MAT237Y1')
   >>> g.add_prerequisites({('MAT135H1', 'MAT136H1'), 'MAT137Y1', 'MAT157Y1'}, 'STA237H1')
   >>> g.get_all_prerequisites('CSC148H1')
   [{'CSC108H1'}]
   >>> len(g.get_all_prerequisites('CSC413H1'))
   18
   >>> for course in {'CHM135H1', 'CHM136H1', 'CHM151Y1', 'BIO120H1', 'BIO130H1', 'HMB265H1', 'BIO230H1'}:
   ...     g.add_course(course)
   >>> for course in {'BCH210H1', 'BCH311H1', 'CSB349H1'}:
   ...     g.add_course(course)
   >>> for course in {'CSC324H1', 'CSC373H1', 'BCB410H1'}:
   ...     g.add_course(course)
   >>> for course in {'CSC263H1', 'CSC236H1', 'CSC165H1'}:
   ...     g.add_course(course)
   >>> g.add_prerequisites({('CSC148H1', 'CSC165H1'), 'CSC111H1'}, 'CSC236H1')
   >>> g.add_prerequisites({'STA237H1'}, 'CSC236H1')
   >>> g.add_prerequisites({'CSC236H1'}, 'CSC263H1')
   >>> g.add_prerequisites({'CSC263H1'}, 'CSC373H1')
   >>> g.add_prerequisites({'CSC263H1'}, 'CSC324H1')
   >>> g.add_prerequisites({'CSC324H1', 'CSC373H1'}, 'BCB410H1')
   >>> g.add_prerequisites({'BCH311H1', 'CSB349H1'}, 'BCB410H1')
   >>> g.add_prerequisites({('CHM135H1', 'CHM136H1'), 'CHM151Y1'}, 'BCH210H1')
   >>> g.add_prerequisites({'BCH210H1'}, 'BCH311H1')
   >>> g.add_prerequisites({'BIO130H1'}, 'BIO230H1')
   >>> g.add_prerequisites({('CHM135H1', 'CHM136H1'), 'CHM151Y1'}, 'BIO230H1')
   >>> g.add_prerequisites({('CHM135H1', 'CHM136H1'), 'CHM151Y1'}, 'HMB265H1')
   >>> g.add_prerequisites({'BIO120H1'}, 'HMB265H1')
   >>> g.add_prerequisites({'BIO130H1'}, 'HMB265H1')
   >>> g.add_prerequisites({'HMB265H1'}, 'CSB349H1')
   >>> g.add_prerequisites({'BIO230H1'}, 'CSB349H1')
   >>> g.add_exclusion('CHM151Y1', {'CHM135H1', 'CHM136H1'})
   >>> g.add_exclusion('CHM135H1', {'CHM151Y1'})
   >>> g.add_exclusion('CHM136H1', {'CHM151Y1'})
   >>> g.add_exclusion('MAT138H1', {'MAT137Y1', 'MAT157Y1'})
   >>> g.add_exclusion('CSC148H1', {'CSC111H1'})
   >>> g.add_exclusion('CSC110Y1', {'CSC108H1', 'CSC148H1', 'CSC165H1'})
   >>> g.add_exclusion('CSC111H1', {'CSC108H1', 'CSC148H1', 'CSC165H1'})
   >>> g.add_exclusion('CSC165H1', {'CSC111H1', 'CSC236H1'})
   >>> g.add_exclusion('CSC108H1', {'CSC111H1', 'CSC110Y1'})
   >>> g.add_corequisites('MAT240H1', {'MAT157Y1'})
   >>> len(g.get_all_prerequisites('BCB410H1'))
   48
   >>> len(g.get_all_prerequisites('BCH311H1'))
   2
   >>> len(g.get_all_prerequisites('BCH210H1'))
   2
   >>> len(g.get_all_prerequisites('CSB349H1'))
   2
   >>> len(g.get_all_prerequisites('CSC324H1'))
   6
   >>> len(g.get_all_prerequisites('CSC263H1'))
   6
   >>> len(g.get_all_prerequisites('CSC236H1'))
   6
   >>> g.get_prerequisites('BCB410H1', {'MAT137Y1', 'CSC110Y1', 'CSC111H1', 'BIO130H1', 'CHM135H1', 'CHM136H1'}, {'CSC324H1'}, 4.0)[0][0]
   3.0
   >>> len(g.get_all_prerequisites('CSC413H1'))
   14
   >>> g.get_prerequisites('MAT237Y1', {'MAT135H1'}, {'MAT137Y1'}, 2.0)

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

    def get_immediate_prerequisites(self, course_code: str) -> list:
        """Gets the prerequisites immediately before a course.
        """

    def get_dependents(self, course_code: str) -> set:
        """Returns a list of courses that are dependents to the given course
        ***DECIDE IF IT SHOULD RETURN A LIST OF _COURSE OR STR (COURSE_CODE)***
        """
        return {course.code for course in self._courses[course_code].dependents}

    def course_to_tree(self, course_code: str) -> Tree:
        """Returns a tree of prerequisites absed on the course code
        """
        return self._courses[course_code].to_tree()


def count_credits(course_set: set[str]) -> int:
    """Count the number of credits in a set of strings\
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
