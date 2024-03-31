"""
Outputs a .csv file in a nice format.
"""

import pandas


def parse(filename: str):
    """reads the file"""
    df = pandas.read_excel(filename)

    for index, row in df.iterrows():
        parse_row(row)


def parse_row(row):
    """
    parses a row
    """
    prerequisites = row['Prerequisites']

    if type(prerequisites) is not float:
        prerequisites = prerequisites.replace(' ', '')
        prerequisites = clean_brackets(prerequisites, False)
        prerequisites = clean_brackets(prerequisites, True)

    # else:
    #     print('NA', prerequisites)


def clean_brackets(s: str, reverse: bool) -> str:
    """
    pass in a string and cleans the brackets
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
    new_s = ''
    i = 0
    while i < len(s):
        char = s[i]
        if char == '(':
            r, num_char = empty_brackets_helper(s[i:])
            new_s += r
            i += num_char

        else:
            new_s += char
            i += 1

    return new_s


def empty_brackets_helper(s: str) -> tuple[str, int]:
    if s == '()':
        return ('', 1)

    new_s = ''
    i = 0

    while i < len(s):
        char = s[i]

        if char == '(':
            r, skip = empty_brackets_helper(s[i + 1:])
            new_s += r
            i += skip
            continue

        elif char == ')':
            if new_s != '':
                return '(' + new_s + ')', i + 2
            else:
                return '', i + 1

        new_s += char
        i += 1
    return new_s, i + 1


if __name__ == '__main__':
    # parse('output.xlsx')
    # print(empty_brackets('a((d)gh)(ij)()'))
    print(empty_brackets('()'))
