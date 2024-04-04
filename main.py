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
# graph = load_graph('clean_data_v3.xlsx')
#
# # Computer Science Specialist
# cs_specialist = Degree('Computer Science Specialist', 'ASSPE1609', 'Specialist')
# required_courses = []

# for course in required_courses:
#     cs_specialist.add_prerequisites()


if __name__ == '__main__':
    graph = load_graph('clean_data_v4.xlsx')

    m = graph.get_prerequisites('MAT237Y1', {'MAT135H1'}, {'MAT137Y1'}, 3.0)
    print(m)
    print(graph.get_prerequisites('STA237H1', {'MAT135H1'}, {'MAT137Y1'}, 3.0))
    print(graph.get_all_prerequisites('STA237H1'))

    p = graph._courses['MAT237Y1'].prerequisites
    print(p.evaluate())

    print(graph.get_all_prerequisites('MAT237Y1'))

    #
    # import doctest
    # doctest.testmod()
    #
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['graph_course', 'degree'],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
