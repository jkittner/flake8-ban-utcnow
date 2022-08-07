import ast
from typing import Any
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type

MSG = "UTC001 don't use datetime.utcnow(), use datetime.now(timezone.utc) instead"  # noqa: E501


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.assignments: List[Tuple[int, int]] = []

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == 'utcnow':
            self.assignments.append((node.lineno, node.col_offset))

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if (
            (
                isinstance(node.value, ast.Attribute) and
                node.attr == 'utcnow' and
                node.value.attr == 'datetime'
            ) or (
                isinstance(node.value, ast.Name) and
                node.attr == 'utcnow' and
                node.value.id == 'datetime'
            )
        ):
            self.assignments.append((node.lineno, node.col_offset))

        self.generic_visit(node)


class Plugin:
    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.assignments:
            yield line, col, MSG, type(self)
