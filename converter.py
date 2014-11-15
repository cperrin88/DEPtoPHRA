__author__ = 'Christopher Perrin'

from nltk import tree


class Converter(object):
    def __init__(self, dep_graph, proj_table, arg_table, mod_table):
        self.dep_graph = dep_graph
        self.proj_table = proj_table
        self.arg_table = arg_table
        self.mod_table = mod_table

    def convert(self):
        head = self._make_projection(self.dep_graph.root)
        deps = self.dep_graph.root['deps']
        self._convert_subtree(deps, head, self.dep_graph.root)
        return head

    def _convert_subtree(self, nodelist, suptree, supnode):
        if len(nodelist) == 0:
            return

        left = list()

        while len(nodelist) > 0 and nodelist[0] < supnode['address']:
            left.insert(0, nodelist.pop(0))

        right = nodelist

        left_tree = suptree
        right_tree = suptree.copy(deep=True)
        for node in left:
            n = self.dep_graph.get_by_address(node)

            proj = self._make_projection(n)

            self._convert_subtree(n['deps'], proj, n)
            if n['rel'] == "ARG":
                left_tree = self._connect_arg_to_head(proj, left_tree, -1)
            elif n['rel'] == "MOD":
                left_tree = self._connect_mod_to_head(proj, left_tree, -1)

        for node in right:
            n = self.dep_graph.get_by_address(node)

            proj = self._make_projection(n)

            self._convert_subtree(n['deps'], proj, n)
            if n['rel'] == "ARG":
                right_tree = self._connect_arg_to_head(proj, right_tree, 1)
            elif n['rel'] == "MOD":
                right_tree = self._connect_mod_to_head(proj, right_tree, 1)

        n = suptree
        r = right_tree
        while len(n) > 0:
            new_n = n[len(n)-1]
            while len(r) > 1:
                n.append(r.pop(1))
            try:
                n = new_n
                r = r[0]
            except:
                break
        return

    def _make_projection(self, node):
        out = SearchableTree(node['word'], list())
        out = SearchableTree(node['tag'], [out])
        if not node['tag'] in self.proj_table.keys():
            return out

        for tag in self.proj_table[node['tag']]:
            out = SearchableTree(tag, [out])
        return out

    def _connect_arg_to_head(self, tree, suptree, pos):
        head_node = suptree.find_fork()

        index = 1
        if pos == -1:
            index = 2

        while head_node is not None:
            if head_node.label() not in self.arg_table.keys() or self.arg_table[head_node.label()][index] == 0:
                head_node = head_node.parent()
                continue
            tree_node = tree.find_fork()
            while tree_node is not None:
                if tree_node.label() in self.arg_table[head_node.label()][2]:
                    tree_node.clear_parent()
                    if pos == -1:
                        head_node.insert(0, tree_node)
                    else:
                        head_node.append(tree_node)

                    return suptree
                tree_node = tree_node.parent()

        raise Exception()

    def _connect_mod_to_head(self, tree, suptree, pos):
        head_node = suptree.find_fork()

        index = 1
        if pos == -1:
            index = 0

        while head_node is not None:
            if head_node.label() not in self.mod_table.keys():
                head_node = head_node.parent()
                continue
            tree_node = tree.find_fork()
            while tree_node is not None:
                if tree_node.label() in self.mod_table[head_node.label()][index]:
                    tree_node.clear_parent()
                    if pos == -1:
                        head_node.insert(0, tree_node)
                    else:
                        head_node.append(tree_node)

                    return suptree
                tree_node = tree_node.parent()

        raise Exception()


class SearchableTree(tree.ParentedTree):
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

    def find_fork(self):
        if len(self) != 1:
            return self

        return self[0].find_fork()

    def clear_parent(self):
        self._parent = None