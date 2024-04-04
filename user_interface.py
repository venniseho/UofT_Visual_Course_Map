"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the code for the user interface.
This will be how the user interacts with the program in the console.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from graph_course import Graph
from plotly_visualization import display_plot


def run_commands(g: Graph) -> None:
    """
    Prints out a list of commands the user can use to interact with our interface.
    """
    commands = ['Get Prerequisites', 'Get Dependents', 'Display Course', 'Browse', 'Help']
    print(f'LIST OF COMMANDS:'
          f'- Get Prerequisites'
          f'- Get Dependents'
          f'- Display Course'
          f'- Help')

    print()

    user_input = input('What would you like to do? ').lower()

    while user_input not in commands:
        user_input = input('Invalid input. What would you like to do? ')

    # action after selecting valid command

    if user_input == 'help':
        course_map_help(commands)



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
