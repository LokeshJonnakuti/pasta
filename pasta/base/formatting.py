# coding=utf-8
"""Operations for storing and retrieving formatting info on ast nodes."""

PASTA_DICT = '__pasta__'


def get(node, name, default=None):
  try:
    return _formatting_dict(node).get(name, default)
  except AttributeError:
    return default


def set(node, name, value):
  if not hasattr(node, PASTA_DICT):
    try:
      setattr(node, PASTA_DICT, {})
    except AttributeError:
      pass
  _formatting_dict(node)[name] = value


def append(node, name, value):
  set(node, name, get(node, name, '') + value)


def prepend(node, name, value):
  set(node, name, value + get(node, name, ''))


def _formatting_dict(node):
  return getattr(node, PASTA_DICT)
