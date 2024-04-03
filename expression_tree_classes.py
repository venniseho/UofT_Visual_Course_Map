"""CSC111 - Project 2: U of T Visual Course Map

Module Description:
This module contains the Expression, Course, and Tree Classes for the Visual Course Map.

Creators:
- Chris Cao
- Ryan Fu
- Vennise Ho
"""
from __future__ import annotations
from typing import Any, Optional


class Tree:
    """A recursive tree data structure.

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
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

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
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.
        """

        return "Tree(" + str(self._root) + ", " + str(self._subtrees.__repr__()) + ")"


class Expr:
    """A general expression in our abstract syntax tree
    """
    code: str

    def __init__(self) -> None:
        pass

    def evaluate(self) -> Any:
        """Evaluates an expression, whetehr it;s a course or a BoolOp"""
        raise NotImplementedError

    def to_tree(self) -> Tree:
        """Return a tree representation of this expression"""
        raise NotImplementedError


class _Course(Expr):
    """A course in a graph (acts as a vertex).

    Instance Attributes:
    - code: the course code (ex. CSC111)
    - prerequisites: the courses that point to this course
    - dependents: the courses that this course points to
    """
    prerequisites: BoolOp
    dependents: set[_Course]

    # extra / implement later
    name: str
    description: str
    breadth: int
    credit: float
    exclusions: set[_Course]
    corequisites: set[_Course]

    def __init__(self, code: str) -> None:
        """Initialize a new course vertex with the given code, prerequisites, and dependents.
        """
        super().__init__()
        self.code = code
        self.prerequisites = BoolOp('and', [])
        self.dependents = set()
        self.credit = 1.0 if code[6] == 'Y' else 0.5
        self.exclusions = set()
        self.corequisites = set()

    def evaluate(self) -> list:
        """Evaluate the course to give itself and its prerequisites
        """
        return combine_lists([{self.code}], self.prerequisites.evaluate())

    def are_exclusions(self, course: _Course) -> bool:
        """Check if self and course are exclusions of each other"""
        return course in self.exclusions and self in course.exclusions

    def to_tree(self) -> Tree:
        """Return a tree of this vertices course prerequisites"""
        if self.prerequisites.operand == []:
            return Tree(self.code, [])
        else:
            if len(self.prerequisites.operand) == 1:
                return Tree(self.code, [self.prerequisites.operand[0].to_tree()])
            else:
                return Tree(self.code, [self.prerequisites.to_tree()])


class BoolOp(Expr):
    """and/or class"""

    operand: list[Expr]

    def __init__(self, operator: str, operands: list[Expr]) -> None:
        super().__init__()
        self.code = operator
        self.operand = operands

    def evaluate(self) -> list:
        """This function returns a list of sets of different possibilities to meet an outcome. For example, if we have
        the BoolOp tree 'and' with operands A, B, and BoolOp('or', [C, D]), then we get
        [{A, B, C}, {A, B, D}]
        """
        if not self.operand:
            return []
        else:
            if self.code == 'and':
                new_list = []
                for operand in self.operand:
                    new_list = combine_lists(new_list, [operand.evaluate()]) \
                        if isinstance(operand.evaluate(), set) \
                        else combine_lists(new_list, operand.evaluate())
            else:
                new_list = []
                for operand in self.operand:
                    new_list = new_list + operand.evaluate() \
                        if isinstance(operand.evaluate(), list) \
                        else new_list + [operand.evaluate()]
            return new_list

    def to_tree(self) -> Tree:
        if self.operand == []:
            return Tree(self.code, [])
        else:
            if len(self.operand) == 1:
                return self.operand[0].to_tree()
            else:
                return Tree(self.code, [ex.to_tree() for ex in self.operand])


def combine_lists(lst1: list[set], lst2: list[set]) -> list:
    """Mutate list 1 such that each set in lst1 has exactly one elemnt of list2
    for as many times as sets in lst2. Lst2 only has sets that have no tuples.
    """
    if not lst1:
        return lst2
    elif not lst2:
        return lst1
    else:
        return [element1.union(element2) for element1 in lst1 for element2 in lst2]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
