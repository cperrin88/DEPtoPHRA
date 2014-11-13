__author__ = 'Christopher Perrin'

from nltk import tree

class Converter(object):
    def __init__(self, dep_graph, proj_table, arg_table, mod_table):
        """:type : nltk.parse.DependencyGraph"""
        self.dep_graph = dep_graph
        self.proj_table = proj_table
        """:type : json"""
        self.arg_table = arg_table
        self.mod_table = mod_table

        print(dep_graph)

    def convert(self):
        phrase_struct = tree.Tree()
        phrase_struct.append()
        self._find_projection(self.dep_graph.root['address'], tree)

    def _find_projection(self, address, phrase_struct):
        node = self.dep_graph.get_by_address(address)
        print(node)

    def _find_anchor(self):
        pass


class Tree(object):
    def __init__(self, children=list(), parent=None):
        self.children = children
        self.parent = parent

    def find(self):
        pass

    def append(self, child):
        self.children.append(child)
