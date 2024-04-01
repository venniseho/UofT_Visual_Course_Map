"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module is the main file.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
import graph_course
from degree import Degree
from file_reader import load_graph

# LOAD GRAPH
graph = load_graph('clean_data.xlsx')

# Computer Science Specialist
cs_specialist = Degree('Computer Science Specialist', 'ASSPE1609', 'Specialist')
required_courses = []

for course in required_courses:
    cs_specialist.add_prerequisites2()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['graph_course', 'degree'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
