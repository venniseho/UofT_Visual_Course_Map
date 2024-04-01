"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module reads the files for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
import pandas
import openpyxl
from graph_course import Graph





def load_graph(excel_file: str) -> None:
    """
    reads an excel file
    """
    graph = Graph()
    dataframe = pandas.read_excel(excel_file)

    for index, row in dataframe.iterrows():

        # course code
        course_code = row['Course Name']
        graph.add_course(course_code)

        # prerequisites
        for

        # corequisites


        # exclusions

    # add dependents
