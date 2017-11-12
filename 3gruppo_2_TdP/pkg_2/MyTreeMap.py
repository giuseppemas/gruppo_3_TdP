from TdP_collections.map.binary_search_tree import TreeMap
'''
Progettare la classe MyTreeMap che espone la stessa interfaccia di TreeMap ma implementa i metodi after() e before() con
complessità di tempo O(1), senza aumentare la complessità di tempo di tutti gli altri metodi.
'''

class MyTreeMap(TreeMap):

    class _Node(TreeMap._Node):
        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right) #in this way we use the linked_binary_tree map init
            self._afterpos = None
            self._beforepos = None

    def _add_node_left(self, p, e):
        """Create a new left child for Position p, storing node e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node._left = e
        e._parent = node
        return self._make_position(node._left)

    def _add_node_right(self, p, e):
        """Create a new right child for Position p, storing node e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node._right = e # node is its parent
        e._parent = node
        return self._make_position(node._right)

    def __setitem__(self, k, v):
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))  # from LinkedBinaryTree
        else:
            p = self.root()
            item = self._Item(k, v)
            node = self._Node(item)
            while p is not None:
                if p.key()==k:
                    p.element()._value = v  # replace existing item's value
                    self._rebalance_access(p)  # hook for balanced tree subclasses
                    return
                elif p.key()<k:
                    if self.right(p) is None:
                        leaf = self._add_node_right(p, node)
                        p._node._afterpos = leaf
                        leaf._node._beforepos = self.parent(leaf)
                        #print("beaforefoglia", leaf._node._beforepos.key(), "foglia", leaf.key())
                    else:
                        if p._node._afterpos.key()>k:
                            p._node._afterpos = self._make_position(node)
                            p._node._afterpos._node._beforepos = p
                        p = self.right(p)
                elif p.key()>k:
                    if self.left(p) is None:
                        leaf = self._add_node_left(p, node)
                        p._node._beforepos = leaf
                        leaf._node._afterpos = self.parent(leaf)
                        #print("afterfoglia", leaf._node._afterpos.key(), "foglia", leaf.key())
                    else:
                        if p._node._beforepos.key()<k:
                            p._node._beforepos = self._make_position(node)
                            p._node._beforepos._node._afterpos = p
                        p = self.left(p)
            self._rebalance_insert(leaf)


    def after(self, p):
        """returns to the successor's position"""
        return p._node._afterpos
    
    def before(self, p):
        """returns the predecessor's position"""
        return p._node._beforepos

    def __str__(self):
        s = ''
        for i in self:
            s += str(i)
            s += '  '

        return s


#################TEST#######################

t = MyTreeMap()
chiavi = [5,2,12,1,3,15,8,7,11,10]
for i in range(len(chiavi)):
    t.__setitem__(chiavi[i],i*i)

for k in t.inorder():
    p = t.find_position(k.key())
    resultafter = t.after(p)
    resultbefore = t.before(p)
    if resultafter == None:
        print("result before", resultbefore.key(), "Position", p.key(), "result after", resultafter)
    elif resultbefore == None:
        print("result before", resultbefore, "Position", p.key(), "result after", resultafter.key())
    else:
        print("result before", resultbefore.key(), "Position", p.key(), "result after", resultafter.key())


