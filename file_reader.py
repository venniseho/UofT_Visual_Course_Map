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
    """
    graph = Graph()
    dataframe = pandas.read_excel(excel_file)

    # add courses as vertices in the graph
    for index, row in dataframe.iterrows():
        # course code
        course_code = row['Course Name']
        graph.add_course(course_code)

    # add everything else (i.e. prerequisites)
    for index, row in dataframe.iterrows():
        # prerequisites
        prerequisites = row['Prerequisites']
        if not isinstance(prerequisites, float):
            prerequisites_list = parse_requisites(prerequisites)

            for subset in prerequisites_list:
                graph.add_prerequisites(subset, row['Course Name'])

        # exclusions
        exclusions = row['Exclusion']
        if not isinstance(exclusions, float):
            exclusions_list = split_string(exclusions)
            for substring in exclusions_list:
                if substring.isalnum():
                    graph.add_exclusion(row['Course Name'], substring)

    return graph


def parse_requisites(s: str) -> list[list]:
    """
    Parses a string of requisites into the format we want.

    >>> parse_requisites('MAT137,CSC110,CSC111')
    [['MAT137'], ['CSC110'], ['CSC111']]
    >>> parse_requisites('MAT137/CSC110/CSC111')
    [['MAT137', 'CSC110', 'CSC111']]
    >>> parse_requisites('MAT137,CSC110/CSC111')
    [['MAT137'], ['CSC110', 'CSC111']]
    >>> parse_requisites('(MAT135,MAT136)')
    [[('MAT135', 'MAT136')]]
    >>> parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111')
    [['MAT137', ('MAT135', 'MAT136')], ['CSC110'], ['CSC111']]
    """

    if s in '':
        return []

    lst = split_string(s)
    i = 1

    if not lst:
        return []

    parse_brackets(lst)
    check_or(lst)

    lst[0] = [lst[0]]

    while i < len(lst):

        if lst[i] == '/':
            lst.pop(i)
            course = lst.pop(i)
            lst[i - 1].append(course)

        elif lst[i] == ',':
            lst.pop(i)
            lst[i] = [lst[i]]
            i += 1

    return lst


def parse_brackets(lst: list) -> None:
    """
    Helper function to parse_requisites that parses brackets specifically.
    Calls parse_brackets_helper as a helper.
    """

    while True:
        try:
            i = lst.index(')')
        except ValueError:
            return lst

        close_bracket_index = i
        open_bracket_index = close_bracket_index

        while lst[open_bracket_index] != '(':
            open_bracket_index -= 1

        parse_brackets_helper(lst, open_bracket_index)


def parse_brackets_helper(lst: list, start: int) -> None:
    """
    Recursive helper for parse_brackets.
    Takes in a list where start is the index of an open bracket recursively parses through the list
    until it hits its corresponding closing bracket.

    Preconditions:
    - lst[start] == '('
    """
    i = start
    lst.pop(i)

    lst[i] = [lst[i]]

    i += 1

    while True:
        if lst[i] == ')':
            break

        if lst[i] == '/':
            lst.pop(i)
            if lst[i] == '(':
                parse_brackets_helper(lst, i)

            if not isinstance(lst[i - 1][-1], list):
                lst[i - 1][-1] = [lst[i - 1][-1]]

            course = lst.pop(i)
            lst[i - 1][-1].append(course)
            continue

        elif lst[i] == ',':
            lst.pop(i)
            if lst[i] == '(':
                parse_brackets_helper(lst, i)
            course = lst.pop(i)
            lst[i - 1].append(course)

    lst.pop(i)
    lst[i - 1] = tuple(lst[i - 1])


def check_or(lst: list) -> None:
    """
    If any elements of the list are tuples containing only one list, drop the tuple brackets.
    - tuples are 'and' but sometimes there is only a slash (meaning or).
    """
    for i in range(len(lst)):
        element = lst[i]
        if ((isinstance(element, list)) and len(element) == 1 and isinstance(element[0], list)):
            lst[i] = lst[i][0]


def split_string(s: str) -> list:
    """
    Splits a string into by comma, forward slash, and brackets and adds each element to a list.

    >>> split_string('(MAT135,MAT136)/MAT137')
    ['(', 'MAT135', ',', 'MAT136', ')', '/', 'MAT137']
    """
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
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'graph_course'],    # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
