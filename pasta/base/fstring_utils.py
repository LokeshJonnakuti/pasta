# coding=utf-8
"""Helpers for working with fstrings (python3.6+)."""

import ast

_FSTRING_VAL_PLACEHOLDER = '__pasta_fstring_val_{index}__'


def get_formatted_values(joined_str):
  """Get all FormattedValues from a JoinedStr, in order."""
  return [v for v in joined_str.values if isinstance(v, ast.FormattedValue)]


def placeholder(val_index):
  """Get the placeholder token for a FormattedValue in an fstring."""
  return _FSTRING_VAL_PLACEHOLDER.format(index=val_index)


def perform_replacements(fstr, values):
  """Replace placeholders in an fstring with subexpressions."""
  for i, value in enumerate(values):
    fstr = fstr.replace(_wrap(placeholder(i)), _wrap(value))
  return fstr


def _wrap(s):
  return '{%s}' % s
