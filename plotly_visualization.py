"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the plotly data visualization for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""

import plotly.graph_objects as go
from plot_class import Plot
from graph_course import Graph


def display_plot(g: Graph, course_code: str) -> None:
    """Given a graph of courses and a course_code, display it visually
    """
    p = Plot(g.course_to_tree(course_code))
    nodes = p.to_dict()
    edges = p.get_edges()
    node_x, node_y, node_text = [], [], []
    for node in nodes:
        node_x.append(nodes[node][0])
        node_y.append(nodes[node][1])
        node_text.append(node.get_root())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=node_x,
                             y=node_y,
                             mode='markers+text',
                             textfont={
                                 'family': "arial",
                                 'size': 8,
                                 'color': "white"},
                             marker={'symbol': 'circle', 'size': 40},
                             text=node_text,
                             showlegend=False,
                             ))
    for edge in edges:
        fig.add_trace(go.Scatter(x=[nodes[e][0] for e in edge],
                                 y=[nodes[e][1] for e in edge],
                                 mode='lines+markers+text',
                                 textfont={
                                     'family': "arial",
                                     'size': 8,
                                     'color': "white"},
                                 marker={'symbol': 'circle', 'size': 40, 'color': '#00A2FF'},
                                 text=[edge[0].get_root(), edge[1].get_root()],
                                 showlegend=False,
                                 ))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations', 'Graph', '_Course', 'Tree', 'BoolOp', 'expression_tree_classes',
                          'plotly.graph_objects', 'Plot', 'graph_course', 'plot_class'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
