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


# def parse_requisites(requisites: str) -> list[set]:
#     """
#     >>> parse_requisites('(MAT135/MAT136)') == [{'MAT136', 'MAT135'}]
#     True
#     >>> parse_requisites('(MAT135,MAT136)') == [{('MAT135', 'MAT136')}]
#     True
#     >>> answer = [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}, {'CSC111'}]
#     >>> parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111') == answer
#     True
#     >>> answer =
#     >>> parse_requisites('MAT137/(MAT135,MAT136),((CSC110,CSC111)/(CSC108/CSC109, CSC165))') == answer
#     """
#     lst = []
#     course_set = set()
#
#     curr = 0        # pointer that tracks where we currently are
#     prev = 0        # pointer that tracks where the start of the current word is
#
#     while curr < len(requisites):
#         char = requisites[curr]
#         if char == '(':
#             end_of_word = requisites.find(')', curr)                          # last index
#             substring = requisites[curr + 1:end_of_word]
#
#             if ',' in substring:
#                 subset_list = requisites[curr + 1:end_of_word].split(',')           # split by comma
#                 course_set.add(tuple(subset_list))
#
#             elif '/' in substring:
#                 subset_list = requisites[curr + 1:end_of_word].split('/')
#                 [course_set.add(element) for element in subset_list]
#
#             curr = end_of_word
#             prev = curr + 1
#
#         elif char == ',':
#             if requisites[prev:curr] != '':
#                 course_set.add(requisites[prev:curr])
#             lst.append(course_set)
#             course_set = set()
#
#             prev = curr + 1
#
#         elif char == '/':
#             if requisites[prev:curr] != '':
#                 course_set.add(requisites[prev:curr])
#             print(course_set)
#
#             prev = curr + 1
#
#         curr += 1
#
#     if requisites[prev:curr] != '':
#         course_set.add(requisites[prev:curr])
#     lst.append(course_set)
#
#     return lst

def parse_requisites(requisites: str) -> list[set]:
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
    requisites_list = split_string(requisites)

    lst = []

    for i in range(len(requisites_list)):
        substring = requisites_list[i]

        if substring == '(':
            return parse_helper(requisites_list[i:])


def parse_helper(sublist) -> list:

    lst = []
    t_lst = []
    subset = set()

    for i in range(len(sublist)):
        substring = sublist[i]

        if substring == '(':
            t = tuple(parse_helper(sublist[i + 1:]))

        elif substring == ',':
            subset.add(sublist[i - 1])
            t_lst.append(subset)
            lst.append(t_lst)

        elif substring == '/':
            subset.add(sublist[i - 1])

        elif substring == ')':
            if sublist[i - 2] == ',':
                lst.append(sublist[i - 1])
            elif sublist[i - 2] == '/':
                subset.add(sublist[i - 1])
                lst.append(subset)
            return lst

    # for substring in requisites_list:

def parse(s: str):
    split_list = split_string(s)

    lst = []
    temp_set = set()

    for i in range(len(split_list) - 1):
        substring = split_list[i]

        if substring == '/':
            temp_set.add(split_list[i - 1])
            temp_set.add(split_list[i + 1])

        if substring == ',':
            if temp_set != set():
                lst.append(temp_set)
                temp_set = set()
            else:
                lst.append({split_list[i - 1]})

    if temp_set != set():
        lst.append(temp_set)
    else:
        lst.append({split_list[-1]})

    return lst



def split_string(s: str) -> list[str]:
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


#     lst = []
#     course_set = set()
#     course_name = ''
#     i = 0
#
#     while i < len(requisites):
#         char = requisites[i]
#         if char == '(':
#             parsed_sublist, skip = parse_prerequisites_helper(requisites[i:], 0)
#
#             for subset in parsed_sublist:
#                 # print('----------------', subset)
#                 if isinstance(subset, set):
#                     course_set = course_set.union(subset)
#
#                 else:
#                     course_set.add(subset)
#
#             i += skip
#
#         elif char == ',':
#             if course_name != '':
#                 course_set.add(course_name)
#             if course_set != set():
#                 lst.append(course_set)
#
#             course_set = set()
#             course_name = ''
#
#         elif char == '/':
#             if course_name != '':
#                 course_set.add(course_name)
#
#             course_name = ''
#
#         # # # # # # # # # # # # # # # # #
#         if char.isalnum():
#             course_name += char
#         i += 1
#
#     if course_name != '':
#         course_set.add(course_name)
#     if course_set != set():
#         lst.append(course_set)
#     return lst
#
#
# def parse_prerequisites_helper(requisites: str, bracket_depth: int) -> (list[set], int):
#     """
#     Recursive helper for parse_prerequisites
#     """
#     lst = []
#     course_set = set()
#     course_name = ''
#     i = 0
#
#     while i < len(requisites):
#         char = requisites[i]
#         if char == '(':
#             parsed_list, skip = parse_prerequisites_helper(requisites[i + 1:], bracket_depth + 1)
#             lst += parsed_list
#             i += skip + 1
#
#             if bracket_depth == 0:
#                 return (lst, i)
#
#             continue
#
#         elif char == ')':
#             course_set.add(course_name)
#             lst.append(course_set)
#             return (lst, i + 2)
#
#         elif char == ',':
#             # parsed list is the rest of the courses after the comma and before the next ')'
#             parsed_list, skip = parse_prerequisites_helper(requisites[i + 1:], bracket_depth)
#
#             if course_name != '':
#                 course_set.add(course_name)
#
#             for subset in parsed_list:
#                 course_set = course_set.union(subset)
#
#             lst.append(tuple(course_set))
#
#             course_set = set()
#             # course_name = ''
#
#             bracket_depth -= 1
#             i += skip
#
#             if bracket_depth == 0:
#                 return (lst, i)
#
#             continue
#
#         elif char == '/':
#             if course_name != '':
#                 course_set.add(course_name)
#                 course_name = ''
#
#         if char.isalnum():
#             course_name += char
#         i += 1
#
#     return (lst, i + 1)


# def check_courses(graph: Graph, course_set: set) -> set:
#     """
#     Check if all courses in course_set are in the graph.
#     If course_set contains tuples, check if each individual course is in the graph.
#     If a course is not in graph, remove it from the set.
#     Returns an edited set.
#     """
#     for element in course_set:
#         if isinstance(element, str):
#             if element in graph.

if __name__ == '__main__':
    # load_graph('clean_data.xlsx')

    # # [{'MAT137'}, {'CSC110'}, {'CSC111'}]
    # print(parse_requisites('MAT137,CSC110,CSC111'))
    #
    # # [{'MAT137', 'CSC110', 'CSC111'}]
    # print(parse_requisites('MAT137/CSC110/CSC111'))
    #
    # # [{'MAT137'}, {'CSC110', 'CSC111'}]
    # print(parse_requisites('MAT137,CSC110/CSC111'))
    #
    # # [{'MAT136', 'MAT135'}]
    # print(parse_requisites('(MAT135/MAT136)'))
    #
    # # [{('MAT135', 'MAT136')}]
    # print(parse_requisites('(MAT135,MAT136)'))
    #
    # # [{('MAT135', 'MAT136'), 'MAT137'}]
    # print(parse_requisites('MAT137/(MAT135,MAT136)'))

    # # [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}]
    # print(parse_requisites('MAT137/(MAT135,MAT136),CSC110'))
    #
    # # [{('MAT135', 'MAT136'), 'MAT137'}, {'CSC110'}, {'CSC111'}]
    # print(parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111'))
    #
    # # [{(('CSC110', 'CSC111'), 'CSC165')}]
    # print(parse_requisites('((CSC110,CSC111)/CSC165, CSC109)'))
    # #
    # # [{'MAT137', ('MAT135', 'MAT136')}, {({(('CSC110', 'CSC111'), 'CSC165')})}]
    # print(parse_requisites('MAT137/(MAT135,MAT136),((CSC110,CSC111),CSC165)'))

    # print(parse_requisites('MAT137/(MAT135,MAT136),CSC110,CSC111'))

    # print(parse_requisites('(a,b)'))

    print(parse('a/b/c,d/e,f'))

    # ((CSC110/CSC111, CSC112) / CSC165, CSC109)
    #
    # (({CSC110, CSC111}, CSC112))
