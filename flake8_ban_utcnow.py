from __future__ import annotations

import ast
from collections.abc import Generator
from typing import Any
from typing import Literal
from typing import TypedDict


class Messages(TypedDict):
    utcnow: str
    utcfromtimestamp: str


MSG: Messages = {
    'utcnow': "UTC001 don't use datetime.datetime.utcnow(), use datetime.datetime.now(datetime.timezone.utc) instead or datetime.now(datetime.UTC) on >= 3.11.",  # noqa: E501,
    'utcfromtimestamp': "UTC002 don't use datetime.datetime.utcfromtimestamp(), use datetime.datetime.fromtimestamp(..., tz=datetime.timezone.utc) instead or datetime.datetime.fromtimestamp(..., tz=datetime.UTC) on >= 3.11.",  # noqa: E501
}


def _check_attr(
        node: ast.Attribute,
        attr: Literal['utcnow', 'utcfromtimestamp'],
) -> tuple[int, int, str] | None:
    if (
        (
            isinstance(node.value, ast.Attribute) and
            node.attr == attr and
            node.value.attr == 'datetime'
        ) or (
            isinstance(node.value, ast.Name) and
            node.attr == attr and
            node.value.id == 'datetime'
        )
    ):
        return (node.lineno, node.col_offset, MSG[attr])
    else:
        return None


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.assignments: list[tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id == 'utcnow':
                self.assignments.append(
                    (node.lineno, node.col_offset, MSG['utcnow']),
                )
            elif node.func.id == 'utcfromtimestamp':  # pragma: no branch
                self.assignments.append(
                    (node.lineno, node.col_offset, MSG['utcfromtimestamp']),
                )
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if msg := _check_attr(node=node, attr='utcnow'):
            self.assignments.append(msg)
        elif msg := _check_attr(node=node, attr='utcfromtimestamp'):
            self.assignments.append(msg)
        self.generic_visit(node)


class Plugin:
    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col, msg in visitor.assignments:
            yield line, col, msg, type(self)
