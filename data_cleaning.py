"""
Outputs a .csv file in a nice format.
"""
import openpyxl
import pandas


def create_clean_data_file(filename: str) -> None:
    """
    Creates a new Excel file containing clean data from filename.
    """
    new_excel_file = openpyxl.Workbook()    # new Excel workbook/file
    new_sheet = new_excel_file.active       # select the default sheet

    df = pandas.read_excel(filename)        # read original Excel file --> dataframe

    # HEADER (COLUMN NAMES):
    # ['Course Name', 'Course Description', 'Hours', 'Prerequisites', 'Corequisites',
    # 'Distribution Requirements', 'Breadth Requirements', 'Exclusion']
    header = list(df.columns)
    new_sheet.append(header)

    courses = []

    # adds to courses list to check if courses exist (check_existence function)
    for index, row in df.iterrows():
        course_code = row[header[0]]
        courses.append(course_code)

    # read data from original Excel sheet and add to new Excel sheet
    for index, row in df.iterrows():
        course_code = row[header[0]]
        course_description = row[header[1]]
        hours = row[header[2]]
        prerequisites = parse_cell(row, header[3], courses)
        corequisites = parse_cell(row, header[4], courses)
        distribution_reqs = row[header[5]]
        breadth_reqs = row[header[6]]
        exclusions = parse_cell(row, header[7], courses)

        data_row = [course_code, course_description, hours, prerequisites, corequisites,
                    distribution_reqs, breadth_reqs, exclusions]

        new_sheet.append(data_row)

    new_excel_file.save("clean_data_v4.xlsx")      # Save the workbook to a file


def parse_cell(row: pandas, column: str, courses: list[str]) -> str:
    """
    Parses a specific cell (row[column]) and returns the cleaned string.
    """
    clean_cell = row[column]

    if not isinstance(clean_cell, float):
        clean_cell = fix_spacing(clean_cell, '/')
        clean_cell = clean_cell.replace(' ', '')

        clean_cell = check_existence(courses, clean_cell)

        # run clean_string thrice to make sure we cleaned the data thoroughly
        clean_cell = clean_string(clean_cell)
        clean_cell = clean_string(clean_cell)
        clean_cell = clean_string(clean_cell)

    else:
        clean_cell = ''

    return clean_cell


def clean_string(s: str) -> str:
    """
    Uses all the cleaning functions (below) to clean s.
    """
    new_s = clean_extra_brackets(s, False)
    new_s = clean_extra_brackets(new_s, True)

    new_s = remove_duplicates(new_s, ',')
    new_s = remove_duplicates(new_s, '/')

    new_s = empty_brackets(new_s)

    new_s = remove_string(new_s, '(,)')
    new_s = remove_string(new_s, '(/)')

    new_s = remove_string(new_s, '/,', ',')
    new_s = remove_string(new_s, ',/', ',')

    new_s = remove_string(new_s, ',)', ')')
    new_s = remove_string(new_s, '/)', ')')

    new_s = remove_string(new_s, '(,', '(')
    new_s = remove_string(new_s, '(/', '(')

    new_s = surrounding_brackets(new_s)
    new_s = surrounding_course(new_s)

    new_s = new_s.strip(",/")

    return new_s


def fix_spacing(s: str, char: str) -> str:
    """
    If there is a space between two seperate courses, replace it with char.
    """
    new_s = s[0]

    for i in range(1, len(s) - 1):
        prev = s[i - 1]
        curr = s[i]
        nxt = s[i + 1]

        if prev.isnumeric() and nxt.isalpha() and curr == ' ':
            new_s += char

        else:
            new_s += s[i]

    new_s += s[-1]

    return new_s


def clean_extra_brackets(s: str, reverse: bool) -> str:
    """
    Cleans the extra (unbalanced) brackets from a string (s).
    If reverse is True, the function cleans extra '(' brackets.
    If reverse is False, the function cleans extra ')' brackets.

    Preconditions:
    - all([char != ' ' for char in s])
    """
    bracket_count = 0
    new_s = ''
    factor = 1
    if reverse:
        s = s[::-1]
        factor = -1

    for char in s:
        if char == '(':
            bracket_count += 1 * factor

        elif char == ')':
            bracket_count -= 1 * factor

        # if bracket_count is negative, we know it's an extra bracket
        if bracket_count < 0:
            bracket_count += 1
            continue

        new_s += char

    if reverse:
        new_s = new_s[::-1]         # new s is backwards

    return new_s


def empty_brackets(s: str) -> str:
    """
    Cleans empty brackets from a string (s).

    Preconditions:
    - sum([1 if char == '(' else -1 if char == ')' else 0 for char in s]) == 0

    (All brackets must be balanced.)

    >>> empty_brackets('a((d)gh)(ij)()')
    'a((d)gh)(ij)'
    >>> empty_brackets('()')
    ''
    >>> empty_brackets('(a)(b)')
    '(a)(b)'
    >>> empty_brackets('(()())')
    ''
    >>> empty_brackets('((()())(a(d)))')
    '((a(d)))'
    >>> empty_brackets('()()(a,()b/(c()(d)),(e))')
    '(a,b/(c(d)),(e))'
    """
    new_s = ''
    i = 0
    while i < len(s):
        char = s[i]
        if char == '(':
            r, num_char = empty_brackets_helper(s[i:], 0)
            new_s += r
            i += num_char

        else:
            new_s += char
            i += 1

    return new_s


def empty_brackets_helper(s: str, bracket_depth: int) -> tuple[str, int]:
    """
    Recursive helper for empty_brackets.

    Preconditions:
    - sum([1 if char == '(' else -1 if char == ')' else 0 for char in s]) == 0

    (All brackets must be balanced.)
    """
    if s == '()':
        return ('', 2)

    new_s = ''
    i = 0

    while i < len(s):
        char = s[i]

        if char == '(':
            r, skip = empty_brackets_helper(s[i + 1:], bracket_depth + 1)
            new_s += r
            i += skip

            if bracket_depth == 0:
                return new_s, i
            continue

        elif char == ')':
            if new_s != '':
                return '(' + new_s + ')', i + 2
            else:
                return '', i + 2

        new_s += char
        i += 1
    return new_s, i + 1


def remove_duplicates(s: str, char: str) -> str:
    """
    Removes duplicates of char from a string (s).

    Preconditions:
    - all([char != ' ' for char in s])
    """
    return char.join([i for i in s.split(char) if i != ''])


def remove_string(s: str, remove_s: str, replace_s: str = '') -> str:
    """
    Removes all instances of remove_s from s and replace it with replace_s.

    >>> my_s = 'MAT235Y1/MAT237Y1/MAT257Y1/(,)/(,)/(,),MAT223H1/MAT224H1/MAT240H1'
    >>> remove_string(my_s, '(,)')
    'MAT235Y1/MAT237Y1/MAT257Y1///,MAT223H1/MAT224H1/MAT240H1'


    Preconditions:
    - all([char != ' ' for char in s])
    """
    return s.replace(remove_s, replace_s)


def check_existence(courses: list[str], requisites: str) -> str:
    """
    Checks if a given course exists in courses and removes it from requisites if it doesn't.

    >>> c = ['CSC111', 'CSC110']
    >>> r = 'MAT137'
    >>> check_existence(c, r)
    ''

    >>> r = 'MAT135/MAT136,CSC111,CSC110'
    >>> check_existence(c, r)
    '/,CSC111,CSC110'


    Preconditions:
    - all([char != ' ' for char in s])
    """
    requisites_list = split_string(requisites)

    i = 0
    while i < len(requisites_list):
        substring = requisites_list[i]
        if substring.isalnum() and substring not in courses:
            requisites_list.pop(i)

        else:
            i += 1

    return ''.join(requisites_list)


def split_string(s: str) -> list:
    """
    Splits a string into by comma, forward slash, and brackets and adds each element to a list.

    >>> split_string('(MAT135,MAT136)/MAT137')
    ['(', 'MAT135', ',', 'MAT136', ')', '/', 'MAT137']

    Preconditions:
    - all([char != ' ' for char in s])
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


def surrounding_brackets(requisites: str) -> str:
    """
    Checks if the elements surrounding brackets are valid.

    >>> s = 'z(MAT135/MAT136,5(CSC111,CSC110)a))'
    >>> surrounding_brackets(s)
    'z,(MAT135/MAT136,5,(CSC111,CSC110),a))'

    Preconditions:
    - all([char != ' ' for char in s])
    """
    requisites_list = split_string(requisites)

    i = 1
    while i < len(requisites_list) - 1:
        substring = requisites_list[i]
        if substring == '(' and not requisites_list[i - 1] in [',', '/', '(']:
            requisites_list.insert(i, ',')

        elif substring == ')' and not requisites_list[i + 1] in [',', '/', ')']:
            requisites_list.insert(i + 1, ',')

        else:
            i += 1

    return ''.join(requisites_list)


def surrounding_course(requisites: str) -> str:
    """
    Checks if the elements surrounding course are valid (specifically the brackets).

    Preconditions:
    - all([char != ' ' for char in s])

    >>> s = '(a)'
    >>> surrounding_course(s)
    'a'

    >>> s = '((ab),c)'
    >>> surrounding_course(s)
    '(ab,c)'
    """
    requisites_list = split_string(requisites)

    i = 1
    while i < len(requisites_list) - 1:
        substring = requisites_list[i]
        if substring.isalnum() and requisites_list[i - 1] == '(' and requisites_list[i + 1] == ')':
            requisites_list.pop(i + 1)
            requisites_list.pop(i - 1)

        else:
            i += 1

        # print(substring, requisites_list)
        # input()

    return ''.join(requisites_list)


if __name__ == '__main__':

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['openpyxl', 'pandas'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
