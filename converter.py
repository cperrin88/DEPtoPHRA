__author__ = 'Christopher Perrin'

from nltk import tree


class Converter(object):
    def __init__(self, dep_graph, proj_table, arg_table, mod_table):
        self.dep_graph = dep_graph
        self.proj_table = proj_table
        self.arg_table = arg_table
        self.mod_table = mod_table

        self.head_tree = self._make_projection(self.dep_graph.root)

    def convert(self):
        self._convert_subtree(self.dep_graph.root['deps'])

    def _convert_subtree(self, nodelist, suptree=None, supnode=None):
        if len(nodelist) == 0:
            return

        for node in nodelist:
            n = self.dep_graph.get_by_address(node)
            proj = self._make_projection(n, suptree, supnode)
            self._convert_subtree(n['deps'], proj, n)
            if suptree is None:
                self._connect_to_head(proj)

    def _make_projection(self, node, suptree=None, supnode=None):
        out = SearchableTree(node['word'], list())
        elem = node['tag']

        while True:
            out = SearchableTree(elem, [out])
            if not suptree is None:
                f = suptree.find_lowest(elem)
                if f != "":
                    if supnode['address'] < node['address']:
                        f.append(out)
                    else:
                        f.insert(-1, out)
                    out = f
                    break

            if not elem in self.proj_table.keys():
                break

            elem = self.proj_table[elem]

        return out

    def _connect_to_head(self, subtree, table):
        print(subtree.pprint())


class SearchableTree(tree.Tree):
    def find(self, string):
        if self.label() == string:
            return self
        for leave in self:
            return leave.find(string)
        return ""

    def find_lowest(self, string):
        for leave in self:
            f = leave.find(string)
            if f != "":
                return f
        if self.label() == string:
            return self
        return ""
