#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# util.py

# --- import -----------------------------------
# import from standard lib
import logging
import re
from pathlib import Path

# import from other lib
import SPARQLWrapper

# > conda forge
# import from my project

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)


# overwrite equality function in class SPARQLWrapper.SmartWrapper.Value
# ----------------------------------------------
def __value_eq__(self, other):
    """check equality of each dictionarys' element"""
    if type(other) is type(self):
        return self.__dict__ == other.__dict__
    return False


setattr(SPARQLWrapper.SmartWrapper.Value, "__eq__", __value_eq__)


# ----------------------------------------------
def combine_dict_in_list(d1_, d2_):
    """
    Merges two dictionaries, non-destructively, combining values on duplicate keys in a list

    >>> d1 = {'a': 'test', 'b': 'btest', 'd': 'dreg'}
    >>> d2 = {'a': ['cool', 'test'], 'b': 'main', 'c': 'clear'}
    >>> combine_dict_in_list(d1,d2)
    {'c': ['clear'], 'a': ['cool', 'test', 'test'], 'b': ['btest', 'main'], 'd': ['dreg']}

    :param d1_: dictionary
    :param d2_: dictionary
    :return: dictionary
    """
    d = {}
    for key in set(list(d1_.keys()) + list(d2_.keys())):
        try:
            if isinstance(d1_[key], (list, set)):
                d.setdefault(key, []).extend(d1_[key])
            else:
                d.setdefault(key, []).append(d1_[key])

        except KeyError:
            pass

        try:
            if isinstance(d2_[key], (list, set)):
                d.setdefault(key, []).extend(d2_[key])
            else:
                d.setdefault(key, []).append(d2_[key])
        except KeyError:
            pass

    return d


def combine_dict_in_set(d1_, d2_):
    """
    Merges two dictionaries, combining values on duplicate keys in a set

    >>> d1 = {'a': 'test', 'b': 'btest', 'd': 'dreg'}
    >>> d2 = {'a': {'cool', 'test'}, 'b': 'main', 'c': 'clear'}
    >>> combine_dict_in_set(d1,d2)
    {'c': {'clear'}, 'a': {'cool', 'test'}, 'b': {'btest', 'main'}, 'd': {'dreg'}}

    :param d1_: dictionary
    :param d2_: dictionary
    :return: dictionary
    """
    if not isinstance(d1_, dict):
        raise TypeError(f" d1_ is not a dictionnary")
    if not isinstance(d2_, dict):
        raise TypeError(f" d2_ is not a dictionnary")
    d = {}
    # for key in set(list(d1_.keys()) + list(d2_.keys())):
    for key in set(d1_.keys()) | set(d2_.keys()):
        try:
            if isinstance(d1_[key], (set, list)):
                d.setdefault(key, set([])).update(d1_[key])
            else:
                d.setdefault(key, set([])).add(d1_[key])

        except KeyError:
            pass

        try:
            if isinstance(d2_[key], (set, list)):
                d.setdefault(key, set([])).update(d2_[key])
            else:
                d.setdefault(key, set([])).add(d2_[key])
        except KeyError:
            pass

    return d


# ----------------------------------------------
def camelCase(word_, sep=" "):
    """rewrite with camelCase format

    >>> word = ["Hello", "World", "Python", "Programming"]
    >>> camelCase(word)
    'helloWorldPythonProgramming'
    >>> word = 'toto_25_tutu'
    >>> camelCase(word, sep='_')
    'toto25Tutu'
    >>> camelCase(word)
    'toto_25_tutu'
    """
    if isinstance(word_, list):
        words = word_
    else:
        words = word_.split(sep=sep)

    s = "".join(word[0].upper() + word[1:].lower() for word in words)
    return s[0].lower() + s[1:]


# ----------------------------------------------
def datasetidCase(filename_):
    """ """
    if not isinstance(filename_, Path):
        filename_ = Path(filename_)
    return camelCase("icos_" + filename_.stem, sep="_")


def filterBracket(name_):
    """ """
    return re.sub(r"(.*)(\[.*\])(.*)", r"\1" r"\3", name_).strip()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
