"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module is the main file.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
import graph_course, degree

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['graph_course', 'degree'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
