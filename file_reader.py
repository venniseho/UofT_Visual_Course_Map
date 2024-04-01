"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module reads the files for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
import pandas
from graph_course import Graph


def load_graph(excel_file: str) -> Graph:
    """
    Loads information from an excel_file into an instance of the graph class.

    'MAT137 / (MAT135,MAT136), CSC110, CSC111'
    [{MAT137, (MAT135, MAT136)}, {CSC110}, {CSC111}]
    """
    graph = Graph()
    dataframe = pandas.read_excel(excel_file)

    # add courses as vertices in the graph
    for index, row in dataframe.iterrows():
        # course code
        course_code = row['Course Code']
        graph.add_course(course_code)

    # add everything else (i.e. prerequisites)
    for index, row in dataframe.iterrows():
        # prerequisites
        prerequisites = row['Prerequisites']
        if not isinstance(prerequisites, float):
            prerequisites_list = parse_requisites(prerequisites)
            print()
            print(row['Course Code'])
            print(prerequisites_list)
            for subset in prerequisites_list:
                print(subset)
                graph.add_prerequisites(subset, row['Course Code'])

        # # corequisites
        # corequisites = row['Corequisites']
        # if not isinstance(corequisites, float):
        #     corequisites_list = parse_requisites(corequisites)
        #
        #     for subset in corequisites_list:
        #         graph.add_corequisites(row['Course Code'], subset)
        #
        # # exclusions
        # exclusions = row['Exclusion']
        # if not isinstance(exclusions, float):
        #     exclusions_list = parse_requisites(exclusions)
        #
        #     for subset in exclusions_list:
        #         graph.add_exclusion(row['Course Code'], subset)

    return graph


def parse_requisites(requisites: str) -> list[set]:
    """
    >>> parse_requisites('(MAT135/MAT136)') == [{'MAT136', 'MAT135'}]
    True
    >>> parse_requisites('(MAT135,MAT136)') == [{('MAT135', 'MAT136')}]
    True
    >>> answer = [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}, {'CSC111'}]
    >>> parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111') == answer
    True
    """
    lst = []
    course_set = set()

    curr = 0        # pointer that tracks where we currently are
    prev = 0        # pointer that tracks where the start of the current word is

    while curr < len(requisites):
        char = requisites[curr]
        if char == '(':
            end_of_word = requisites.find(')', curr)                          # last index
            substring = requisites[curr + 1:end_of_word]

            if ',' in substring:
                subset_list = requisites[curr + 1:end_of_word].split(',')           # split by comma
                course_set.add(tuple(subset_list))

            elif '/' in substring:
                subset_list = requisites[curr + 1:end_of_word].split('/')
                [course_set.add(element) for element in subset_list]

            curr = end_of_word
            prev = curr + 1

        elif char == ',':
            if requisites[prev:curr] != '':
                course_set.add(requisites[prev:curr])
            lst.append(course_set)
            course_set = set()

            prev = curr + 1

        elif char == '/':
            if requisites[prev:curr] != '':
                course_set.add(requisites[prev:curr])

            prev = curr + 1

        curr += 1

    if requisites[prev:curr] != '':
        course_set.add(requisites[prev:curr])
    lst.append(course_set)

    return lst


if __name__ == '__main__':
    load_graph('clean_data.xlsx')
