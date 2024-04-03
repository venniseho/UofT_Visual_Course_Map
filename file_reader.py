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
import re


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

            for subset in prerequisites_list:
                graph.add_prerequisites(subset, row['Course Code'])

        # corequisites
        corequisites = row['Corequisites']
        if not isinstance(corequisites, float):
            corequisites_list = parse_requisites(corequisites)

            for subset in corequisites_list:
                graph.add_corequisites(row['Course Code'], subset)

        # exclusions
        exclusions = row['Exclusion']
        if not isinstance(exclusions, float):
            exclusions_list = parse_requisites(exclusions)

            for subset in exclusions_list:
                graph.add_exclusion(row['Course Code'], subset)

    return graph

def parse_requisites(s: str):
    """
    >>> parse_requisites('MAT137,CSC110,CSC111') == [{'MAT137'}, {'CSC110'}, {'CSC111'}]
    True
    >>> parse_requisites('MAT137/CSC110/CSC111') == [{'MAT137', 'CSC110', 'CSC111'}]
    True
    >>> parse_requisites('MAT137,CSC110/CSC111') == [{'MAT137'}, {'CSC110', 'CSC111'}]
    True
    >>> parse_requisites('(MAT135/MAT136)') == [{'MAT136', 'MAT135'}]
    True
    >>> answer = [{({'MAT224H1', 'MAT247H1'}, 'MAT337H1'), 'MAT357H1'}]
    >>> parse_requisites('(MAT224H1/MAT247H1,MAT337H1)/MAT357H1') == answer
    True
    >>> parse_requisites('(MAT135,MAT136)') == [{('MAT135', 'MAT136')}]
    True
    >>> answer = [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}, {'CSC111'}]
    >>> parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111') == answer
    True
    >>> answer =
    >>> parse_requisites('MAT137/(MAT135,MAT136),((CSC110,CSC111)/(CSC108/CSC109, CSC165))') == answer
    """

    if s in '':
        return []

    lst = split_string(s)
    i = 1

    if not lst:
        return []

    brackets(lst)

    lst[0] = {lst[0]}

    while i < len(lst):

        if lst[i] == '/':
            lst.pop(i)
            course = lst.pop(i)
            lst[i - 1].add(course)

        elif lst[i] == ',':
            lst.pop(i)
            lst[i] = {lst[i]}
            i += 1

    return lst


def brackets(lst):

    while True:
        try:
            i = lst.index(')')
        except ValueError:
            return lst

        close_bracket_index = i
        open_bracket_index = close_bracket_index

        while lst[open_bracket_index] != '(':
            open_bracket_index -= 1

        parse2_helper(lst, open_bracket_index)


def parse2_helper(lst: list, start: int):
    """
    Preconditions:
    - lst only contains one set of brackets (beginning and end)
    - lst[start] == '('
    """
    i = start
    lst.pop(i)

    if lst[i + 1] == '/':
        lst[i] = {lst[i]}

    elif lst[i + 1] == ',':
        lst[i] = [lst[i]]

    i += 1

    while True:
        if lst[i] == ')':
            break

        if lst[i] == '/':
            lst.pop(i)
            if isinstance(lst[i - 1], set):
                course = lst.pop(i)
                lst[i - 1].add(course)

            if isinstance(lst[i - 1], list):
                if not isinstance(lst[i - 1][-1], set):
                    lst[i - 1][-1] = {lst[i - 1][-1]}

                course = lst.pop(i)
                lst[i - 1][-1].add(course)

            # course = lst.pop(i)
            # lst[i - 1].append(course)
            continue

        elif lst[i] == ',':
            lst.pop(i)
            course = lst.pop(i)
            lst[i - 1].append(course)

    lst.pop(i)
    lst[i - 1] = tuple(lst[i - 1])


def split_string(s: str) -> list:
    split_lst = []
    curr_str = ''
    for char in s:
        if char in [',', '/', '(', ')']:
            if curr_str != '':
                split_lst.append(curr_str)
                curr_str = ''

            split_lst.append(char)

        else:
            curr_str += char

    if curr_str != '':
        split_lst.append(curr_str)

    return split_lst

if __name__ == '__main__':
    # load_graph('clean_data.xlsx')

    # [{'MAT137'}, {'CSC110'}, {'CSC111'}]
    print(parse_requisites('MAT137,CSC110,CSC111'))

    # [{'MAT137', 'CSC110', 'CSC111'}]
    print(parse_requisites('MAT137/CSC110/CSC111'))

    # [{'MAT137'}, {'CSC110', 'CSC111'}]
    print(parse_requisites('MAT137,CSC110/CSC111'))

    # [{'MAT136', 'MAT135'}]
    print(parse_requisites('(MAT135/MAT136)'))

    # [{('MAT135', 'MAT136')}]
    print(parse_requisites('(MAT135,MAT136)'))

    # [{('MAT135', 'MAT136'), 'MAT137'}]
    print(parse_requisites('MAT137/(MAT135,MAT136)'))

    # [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}]
    print(parse_requisites('MAT137/(MAT135,MAT136),CSC110'))

    # [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}, {'CSC111'}]
    print(parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111'))

    # [{(('CSC110', 'CSC111'), 'CSC165')}]
    print(parse_requisites('(CSC110,CSC111)/CSC165, CSC109'))
    #
    # [{'MAT137', ('MAT135', 'MAT136')}, {({(('CSC110', 'CSC111'), 'CSC165')})}]
    print(parse_requisites('MAT137/(MAT135,MAT136),((CSC110,CSC111),CSC165)'))

    print(parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111'))

    print(parse_requisites('(a,b)'))

    print(parse_requisites('a/b/c,d/e,(f,g)'))
    print(parse_requisites('(f,g)'))
    print(parse_requisites('(a,(b,c))'))
    # print(parse2('(a,(b,c/d))'))

    # ((CSC110/CSC111, CSC112) / CSC165, CSC109)
    #
    # (({CSC110, CSC111}, CSC112))
