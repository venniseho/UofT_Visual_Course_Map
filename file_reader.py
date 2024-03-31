"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module reads the files for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
import pandas
import openpyxl
from graph_course import Graph


def remove_spaces(string: str) -> str:
    """
    Returns a string with all the spaces removed from it.

    >>> s = 'WRR103H1 / WRR104H1 , WRR201H1 , WRR203H1 , WRR303H1 , WRR305H1 , WRR413H1 , WRR414H1'
    >>> remove_spaces(s)
    'WRR103H1/WRR104H1,WRR201H1,WRR203H1,WRR303H1,WRR305H1,WRR413H1,WRR414H1'
    """
    new_string = ''
    for letter in string:
        if letter != ' ':
            new_string += letter

    return new_string


def parse_prerequisites(prereq_str: str, graph: Graph, course_code: str) -> None:
    """
    Returns a set of prerquisite options based on how the u of t prerequisite string works.

    Preconditions:
    - all([letter != ' ' for letter in prerequisite_str])

    'MAT137 / (MAT135,MAT136), CSC110, CSC111'
    [{MAT137, (MAT135, MAT136)}, {CSC110}, {CSC111}]
    """
    prereqs = set()
    prereq_name = ''

    i = 0

    while i < len(prereq_str):
        if prereq_str[i] == '(':
            index_of_close = prereq_str[i:].index(')')          # index of the closed bracket
            substring = prereq_str[i:index_of_close + 1]            # the substring containing the ()
            lst = []

            for letter in substring:
                if letter == '/':
                    prereq

            i = index_of_close

        elif prereq_str[i] == '/':
            prereqs.add(prereq_name)
            prereq_name = ''

        elif prereq_str[i] == ',':
            graph.add_prerequisites2(prereqs, course_code)
            prereqs = set()

        else:
            prereq_name += prereq_str[i]

        i += 1


def load_graph(excel_file: str) -> None:
    """
    reads an excel file
    """
    graph = Graph()
    dataframe = pandas.read_excel(excel_file)

    for index, row in dataframe.iterrows():

        # course code
        course_code = row['Course Name']
        graph.add_course(course_code)

        # prerequisites
        if not row['Prerequisites'].isinstance(float):
            prerequisites_str = remove_spaces(row['Prerequisites'])
            parse_prerequisites(prerequisites_str, graph, course_code)

        # corequisites


        # exclusions

    # add dependents
