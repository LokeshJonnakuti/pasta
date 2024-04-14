# coding=utf-8
"""Inline constants in a python module."""

import ast
import copy

from pasta.base import ast_utils
from pasta.base import scope


class InlineError(Exception):
  pass


def inline_name(t, name):
  """Inline a constant name into a module."""
  sc = scope.analyze(t)
  name_node = sc.names[name]

  # The name must be a Name node (not a FunctionDef, etc.)
  if not isinstance(name_node.definition, ast.Name):
    raise InlineError('%r is not a constant; it has type %r' % (
        name, type(name_node.definition)))

  assign_node = sc.parent(name_node.definition)
  if not isinstance(assign_node, ast.Assign):
    raise InlineError('%r is not declared in an assignment' % name)

  value = assign_node.value
  if not isinstance(sc.parent(assign_node), ast.Module):
    raise InlineError('%r is not a top-level name' % name)

  # If the name is written anywhere else in this module, it is not constant
  for ref in name_node.reads:
    if isinstance(getattr(ref, 'ctx', None), ast.Store):
      raise InlineError('%r is not a constant' % name)

  # Replace all reads of the name with a copy of its value
  for ref in name_node.reads:
    ast_utils.replace_child(sc.parent(ref), ref, copy.deepcopy(value))

  # Remove the assignment to this name
  if len(assign_node.targets) == 1:
    ast_utils.remove_child(sc.parent(assign_node), assign_node)
  else:
    tgt_list = [tgt for tgt in assign_node.targets
                if not (isinstance(tgt, ast.Name) and tgt.id == name)]
    assign_node.targets = tgt_list
