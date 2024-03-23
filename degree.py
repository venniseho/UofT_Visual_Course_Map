"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the Degree Class for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""


class Degree:
    """
    A degree at the University of Toronto.

    Instance Attributes:
    - name: the name of the degree
    - degree_type: the type of degree (i.e. major, minor, specialist, focus)
    - required_courses: a list of course codes that are required to complete the degree
                        sets are used to indicate options for courses
    """

    name: str
    required_courses: list[set[str]]

    # to implement later
    degree_type: str

    def __init__(self, degree_name: str):
        self.name = degree_name
        self.required_courses = []


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
