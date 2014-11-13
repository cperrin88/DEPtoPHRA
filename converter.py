__author__ = 'Christopher Perrin'

from nltk import tree


class Converter(object):
    def __init__(self, dep_graph, proj_table, arg_table, mod_table):
        self.dep_graph = dep_graph
        self.proj_table = proj_table
        self.arg_table = arg_table
        self.mod_table = mod_table

    def convert(self):
        self.head_tree = self._make_projection(self.dep_graph.root)
        self._convert_subtree(self.dep_graph.root['deps'])

    def _convert_subtree(self, nodelist, suptree=None):
        if len(nodelist) == 0:
            return

        for node in nodelist:
            n = self.dep_graph.get_by_address(node)
            proj = self._make_projection(n, suptree)
            self._connect_to_head(proj)
            self._convert_subtree(n['deps'], proj)

    def _make_projection(self, node, suptree=None):
        out = SearchableTree(node['word'], list())
        elem = node['tag']

        while elem in self.proj_table.keys():
            out = SearchableTree(elem, [out])
            elem = self.proj_table[elem]

        if not suptree is None:
            pass
        return SearchableTree(elem, [out])

    def _connect_to_head(self, subtree):
        pass


class SearchableTree(tree.Tree):

    def find(self, string):
        if self.label() == string:
            return self
        for leave in self.leaves():
            return leave.find(string)
        return ""

    def find_lowest(self, string):
        for leave in self.leaves():
            return leave.find(string)
        if self.label() == string:
            return self
        return ""
