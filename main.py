"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module is the main file.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
import pprint
from graph_course import Graph
from file_reader import load_graph
from plotly_visualization import display_plot


def run_commands(g: Graph) -> None:
    """
    Prints out a list of commands the user can use to interact with our interface.
    """
    commands = ['prerequisites', 'display', 'help', "quit"]
    print('LIST OF COMMANDS:\n'
          '- prerequisites\n'
          '- display\n'
          '- help\n'
          '- quit\n')

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
            course = input("Which course do you want the prerequisites for?").upper()
            if g.valid_course(course):
                pprint.pp(g.get_prerequisites(course, set(), set(), 20.0))
            else:
                print("Not a valid course name!")
        user_input = input('What would you like to do? ').lower()

    # action after selecting valid command


def course_map_help(commands: list) -> None:
    """
    Prints out a description of each command.
    """
    user_input = input('What command would you like help with? ')

    while user_input not in commands:
        user_input = input('Invalid input. What would command would you like help with?? ')

    if user_input == 'prerequisites':
        print('Gets the prerequisites needed for a given course.\n '
              'Once you type this command in, you will be prompted to provide a course.\n'
              'The algorithm will provide a list of possible pathways as prerequisites for the course you typed in\n'
              'along with the credits each pathway will take.')

    elif user_input == 'display':
        print('Displays the given course visually, along with its prerequisites and dependents.\n'
              'Once you type this command in, you will be prompted to provide a course.\n'
              'The algorithm will display the graph of the course you typed in visually (a new window will pop up).'
              'If the system outputs an empty list, no prerequisites are needed.\n')

    elif user_input == 'quit':
        print('Ends the program.')

    elif user_input == 'help':
        print('Outputs descriptions of each command.')


if __name__ == '__main__':
    graph = load_graph('clean_data_v4.xlsx')
    run_commands(graph)

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['graph_course', 'degree', 'file_reader', 'plotly_visualization', 'pprint'],
        'allowed-io': ['print', 'pprint', 'input'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
