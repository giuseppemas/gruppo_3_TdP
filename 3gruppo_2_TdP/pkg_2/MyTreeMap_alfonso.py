from TdP_collections.map.binary_search_tree import TreeMap

'''
Progettare la classe MyTreeMap che espone la stessa interfaccia di TreeMap ma implementa i metodi after() e before() con
complessità di tempo O(1), senza aumentare la complessità di tempo di tutti gli altri metodi.
'''

class MyTreeMap(TreeMap):

    class _Node(TreeMap._Node):
        def __init__(self, element, parent=None, left=None, right=None):
            super()._init(self,element,parent,left,right)
            self._afterpos = None
            self._beforepos = None


    def _subtree_search(self, p, k):
        if k == p.key():
            return p

        elif k < p.key():  # search left subtree
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:  # search right subtree
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p

        newNode = self._Node(None)
        current = self._root
        while current is not None:

            if k < current._afterpos or current._afterpos is None:
                current._afterpos = newNode
                newNode._beforepos = current

            if k > current._beforepos or current._afterpos is None:
                current._beforepos = newNode
                newNode._afterpos = current

            if k == p.key():
                return self._make_position(current)
            elif k < p.key():
                current = current._left
            elif k > p.key():
                current = current._right

        return self._make_position(current)



    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))  # from LinkedBinaryTree
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v  # replace existing item's value
                self._rebalance_access(p)  # hook for balanced tree subclasses
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self._add_right(p, item)  # inherited from LinkedBinaryTree
                else:
                    leaf = self._add_left(p, item)  # inherited from LinkedBinaryTree
        self._rebalance_insert(leaf)  # hook for balanced tree subclasses

