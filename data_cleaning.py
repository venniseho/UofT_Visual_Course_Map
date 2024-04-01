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
    header = [col for col in df.columns]
    new_sheet.append(header)

    # read data from original Excel sheet and add to new Excel sheet
    for index, row in df.iterrows():
        course_code = row[header[0]]
        course_description = row[header[1]]
        hours = row[header[2]]
        prerequisites = parse_cell(row, header[3])
        corequisites = parse_cell(row, header[4])
        distribution_reqs = row[header[5]]
        breadth_reqs = row[header[6]]
        exclusions = parse_cell(row, header[7])

        data_row = [course_code, course_description, hours, prerequisites, corequisites,
                    distribution_reqs, breadth_reqs, exclusions]

        new_sheet.append(data_row)

    new_excel_file.save("clean_data.xlsx")      # Save the workbook to a file


# def parse_file(filename: str) -> list[list[str]]:
#     """
#     Parses the file and turns it into a list of lists.
#     Each sublist will be a row in the new Excel file
#     """
#     df = pandas.read_excel(filename)
#
#     # HEADER (COLUMN NAMES):
#     # ['Course Name', 'Course Description', 'Hours', 'Prerequisites', 'Corequisites',
#     # 'Distribution Requirements', 'Breadth Requirements', 'Exclusion']
#     header = [col for col in df.columns]
#     data_list = [header]
#
#     for index, row in df.iterrows():
#         course_code = row[header[0]]
#         course_description = row[header[1]]
#         hours = row[header[2]]
#         prerequisites = parse_cell(row, header[3])
#         corequisites = parse_cell(row, header[4])
#         distribution_reqs = row[header[5]]
#         breadth_reqs = row[header[6]]
#         exclusions = parse_cell(row, header[7])
#
#         data_row = [course_code, course_description, hours, prerequisites, corequisites,
#                     distribution_reqs, breadth_reqs, exclusions]
#         print(prerequisites)
#
#         data_list += data_row
#
#     return data_list


def parse_cell(row: pandas, column: str) -> str:
    """
    Parses a specific cell (row[column]) and returns the cleaned string
    """
    clean_cell = row[column]

    if type(clean_cell) is not float:
        clean_cell = fix_spacing(clean_cell, '/')
        clean_cell = clean_cell.replace(' ', '')

        # run clean_row twice to make sure we cleaned the data thoroughly
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
    """
    bracket_count = 0
    new_s = ''
    factor = 1
    if reverse:
        s = s[::-1]
        factor = -1

    for i in range(len(s)):
        char = s[i]
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
    """
    return char.join([i for i in s.split(char) if i != ''])


def remove_string(s: str, remove_s: str, replace_s: str = '') -> str:
    """
    Removes all instances of remove_s from s and replace it with replace_s.
    >>> my_s = 'MAT235Y1/MAT237Y1/MAT257Y1/(,)/(,)/(,),MAT223H1/MAT224H1/MAT240H1'
    >>> remove_string(my_s, '(,)')
    'MAT235Y1/MAT237Y1/MAT257Y1///,MAT223H1/MAT224H1/MAT240H1'
    """
    return s.replace(remove_s, replace_s)


if __name__ == '__main__':
    create_clean_data_file('output.xlsx')
