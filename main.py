"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module is the main file.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from graph_course import Graph
from degree import Degree
from file_reader import load_graph
from plotly_visualization import display_plot


# LOAD GRAPH
# graph = load_graph('clean_data_v3.xlsx')
#
# # Computer Science Specialist
# cs_specialist = Degree('Computer Science Specialist', 'ASSPE1609', 'Specialist')
# required_courses = []

# for course in required_courses:
#     cs_specialist.add_prerequisites()


def run_commands(g: Graph) -> None:
    """
    Prints out a list of commands the user can use to interact with our interface.
    """
    commands = ['Get Prerequisites', 'Display Course', 'Help', "Quit"]
    print(f'LIST OF COMMANDS:'
          f'- Get Prerequisites'
          f'- Display Course'
          f'- Help'
          f'- Quit')

    print()

    user_input = input('What would you like to do? ').lower()

    while user_input != "quit":
        if user_input == 'help':
            course_map_help(commands)
        elif user_input == "display":
            course = input("Which course would you like to display?")
            if g.valid_course(course):
                display_plot(g, course)
            else:
                print("Not a valid course name!")

        elif user_input == "prerequisites":
            course = input("Which course do you want the prerequistes for?").upper()
            if g.valid_course(course):
                print(g.get_prerequisites(course, set(), set(), 20.0))
            else:
                print("Not a valid course name!")
        user_input = input('What would you like to do? ').lower()

    # action after selecting valid command


def course_map_help(commands) -> None:
    """
    Tells the user what each command does.
    """
    user_input = input('What command would you like help with? ')

    while user_input not in commands:
        user_input = input('Invalid input. What would command would you like help with?? ')

    if user_input == 'Get Prerequisites':
        print(f'Gets the prerequisites needed for a given course. '
              f'Once you type this command in, you will be prompted to provide a course.'
              f'The algorithm will provide a list of courses required as prerequisites for the course you typed in and '
              f'will also display this graph visually (a new window will pop up).')

    elif user_input == ' Get Dependents':
        print(f'Gets the dependents of a given course. '
              f'Once you type this command in, you will be prompted to provide a course.'
              f'The algorithm will provide a list of courses that require the course you typed in as a prerequisite and'
              f'will also display this graph visually (a new window will pop up).')

    elif user_input == 'Display Course':
        print(f'Displays the given course visually, along with its prerequisites and dependents. '
              f'Once you type this command in, you will be prompted to provide a course.'
              f'The algorithm will display the graph of the course you typed in visually (a new window will pop up).')


"""
What prerequisites are needed to take a particular course?
"""

"""
What is the given a course a prerequisites for?
"""

"""
Display courses
"""

if __name__ == '__main__':
    graph = load_graph('clean_data_v4.xlsx')

    run_commands(graph)

    m = graph.get_prerequisites('MAT237Y1', {'MAT135H1'}, {'MAT137Y1'}, 3.0)
    print(m)
    print(graph.get_prerequisites('STA237H1', {'MAT135H1'}, {'MAT137Y1'}, 3.0))
    print(graph.get_all_prerequisites('STA237H1'))

    # p = graph._courses['MAT237Y1'].prerequisites
    # print(p.evaluate())

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
