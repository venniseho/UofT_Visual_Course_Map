"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the data visualization for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from __future__ import annotations
from typing import Optional, Any
from expression_tree_classes import Tree


class Plot():
    """A recursive tree data structure with a coordinate system to plot the tree.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    #   -_x:
    #       The x coordinate of this tree node
    #   -_y:
    #       The y coordinate of this tree node
    #   -_mod:
    #       A temporary shift value.
    #       This is used to tabulate shifts needed to ensure the tree is centered and non-overlapping.
    _root: Optional[Any]
    _x: float
    _mod: float
    _y: int
    _subtrees: list[Plot]

    def __init__(self, tree: Tree) -> None:
        """Takes in a tree and converts it to a plot with assigned x and y values
        Preconditions:
            - tree.is_empty() == False
        """
        self._root = tree._root
        self._x, self._mod = -1, -1
        self._subtrees = [Plot(subtree) for subtree in tree._subtrees]
        self._y = -1
        self.assign_coordinates()

    def get_root(self) -> Any:
        """Return the root of this tree"""
        return self._root

    def assign_coordinates(self) -> None:
        """Updates the coordinates for the plot. This uses first, second, and thrid pass similar to
        The Reingold Tilford Algorithm described in the following reference
        Wong, K. J. (2023, September 25). Reingold Tilford Algorithm explained with walkthrough. Medium.
        https://towardsdatascience.com/reingold-tilford-algorithm-explained-with-walkthrough-be5810e8ed93
        """
        self._y = self.depth() - 1
        self.assign_y()
        self.first_pass()
        self.second_pass()
        self.third_pass()

    def to_dict(self) -> dict:
        """Return a dictionary mapping a node to its coordinate in our plot"""
        dict_so_far = {self: (self._x, self._y)}
        for subtree in self._subtrees:
            dict_so_far.update(subtree.to_dict())
        return dict_so_far

    def get_edges(self) -> list:
        """Return a set of all the edges in this plot"""
        edges_so_far = []
        for subtree in self._subtrees:
            edges_so_far.append((self, subtree))
            edges_so_far += subtree.get_edges()
        return edges_so_far

    def assign_y(self) -> None:
        """Assign y coordinates of our plot. This assigns a y coordinate based on how far it is form the root,
        where the root has y coordinate of the depth of the tree. If it is 1 away form the root, its y value
        is the root y value minus 1."""
        for subtree in self._subtrees:
            subtree._y = self._y - 1
            subtree.assign_y()

    def first_pass(self) -> None:
        """First pass of update coordinates.
        """
        if self._subtrees == []:
            self._x = 0
            self._mod = 0
        else:
            for subtree in self._subtrees:
                subtree.first_pass()
            for i in range(len(self._subtrees)):
                self._subtrees[i]._x = self._subtrees[0]._x + i
                self._subtrees[i]._mod = self._subtrees[0]._x + i - self._subtrees[i].midpoint()
                if self._subtrees[i]._subtrees == []:
                    self._subtrees[i]._mod = 0
            self._x = self.midpoint()
            self._mod = 0

    def second_pass(self) -> None:
        """Performs the second pass of assign coordinates.
        The second pass takes the mod and shifts all of its children, but not itself, by mod"""
        if self._subtrees == []:
            return
        else:
            for subtree in self._subtrees:
                subtree.shift(self._mod)
                subtree.second_pass()

    def shift(self, degree: float) -> None:
        """Shift itself and its children by a degree"""
        if self._subtrees == []:
            self._x += degree
        else:
            self._x += degree
            for subtree in self._subtrees:
                subtree.shift(degree)

    def third_pass(self) -> None:
        """Peforms the third pass of assign coordinates.
        This pass checks for overlap between subtrees and shifts them accordingly to ensure at each level,
        all trees are 1 unti apart"""
        if self._subtrees == []:
            return
        else:
            for subtree in self._subtrees:
                subtree.third_pass()

            for i in range(1, len(self._subtrees)):
                max_shift_so_far = 0
                max_index = 0
                for d in range(self._y):
                    for s in range(i):
                        max_shift_so_far = self._subtrees[s].get_shift_at_level(self._subtrees[i],
                                                                                d) if max_shift_so_far < self._subtrees[
                            s].get_shift_at_level(self._subtrees[i], d) else max_shift_so_far
                        max_index = s

                for k in range(1, len(self._subtrees)):
                    shift = max_shift_so_far / (i - max_index)
                    self._subtrees[k].shift(shift * k)

            self._x = self.midpoint()

    def get_shift_at_level(self, other: Plot, level: int) -> float:
        """Gets the shift needed at a particular level"""
        if self.max_at_level(level) is None or other.min_at_level(level) is None:
            return 0
        elif self.max_at_level(level) + 1 > other.min_at_level(level):
            return self.max_at_level(level) + 1 - other.min_at_level(level)
        else:
            return 0

    def max_at_level(self, level: int) -> Any:
        """Finds the max x value at a level"""
        if self._y == level:
            return self._x
        elif self._subtrees == [] or self._y < level or all(
                sub.max_at_level(level) is None for sub in self._subtrees):
            return None
        else:
            max_so_far = 0
            for subtree in self._subtrees:
                if subtree.max_at_level(level) is not None:
                    if max_so_far < subtree.max_at_level(level):
                        max_so_far = subtree.max_at_level(level)
            return max_so_far

    def min_at_level(self, level: int) -> Any:
        """Finds the min x value at a level"""
        if self._y == level:
            return self._x
        elif self._subtrees == [] or self._y < level or all(
                sub.min_at_level(level) is None for sub in self._subtrees):
            return None
        else:
            min_so_far = 1000000
            for subtree in self._subtrees:
                if subtree.min_at_level(level) is not None:
                    if min_so_far > subtree.min_at_level(level):
                        min_so_far = subtree.min_at_level(level)
            return min_so_far

    def depth(self) -> int:
        """Return the number of items contained in this tree.
        """
        if self.is_empty():
            return 0
        elif self._subtrees == []:
            return 1
        else:
            return max({subtree.depth() for subtree in self._subtrees}) + 1

    def midpoint(self) -> float:
        """Returns the midpoint of a trees subtree x coordinates if the tree has children
        Preconditions:
            - self._subtrees != []
        """
        if self._subtrees == []:
            return 0.0
        else:
            return sum([subtree._x for subtree in self._subtrees]) / len(self._subtrees)

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._y}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations', '_Course', 'Tree', 'BoolOp', 'expression_tree_classes'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
