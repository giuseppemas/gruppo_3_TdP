from pkg_2.MyTreeMap import MyTreeMap
'''
    Progettare la classe MyAVLTreeMap, derivata da MyTreeMap, che implementa tutti i metodi della classe padre garantendo
    almeno le stesse complessità di tempo di AVLTreeMap.
    '''

class MyAVLTreeMap(MyTreeMap):
    """Sorted map implementation using an AVL tree."""
    
    # ---------------------------- nested _Node class ----------------------------
    class _Node(MyTreeMap._Node):
        __slots__ = 'height'
        
        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right) #in this way we use the linked_binary_tree map init
            self._height = 0
        
        def left_height(self):
            return self._left._height if self._left is not None else 0
        
        def right_height(self):
            return self._right._height if self._right is not None else 0
    
    # --------------------- positional-based private methods ---------------------
    
    def _recompute_height(self, p):
        p._node._height = 1 + max(p._node.left_height(), p._node.right_height())
    
    def _isbalanced(self, p):
        return abs(p._node.left_height() - p._node.right_height()) <= 1
    
    def _tall_child(self, p, favorleft=False): #this parameter controls tiebrecker (spareggio)
        if p._node.left_height() + (1 if favorleft else 0) > p._node.right_height():
            return self.left(p)
        else:
            return self.right(p)

    def _tall_grandchild(self, p):
        child = self._tall_child(p)
        #if child is on left, favor left grandchild; else favor right grandchild
        alignment = (child == self.left(p))
        return self._tall_child(child, alignment) #in this case we have a favorleft != False
    
    def _rebalance(self, p):
        while p is not None:
            old_height = p._node._height
            if not self._isbalanced(p):
                p = self._restructure(self._tall_grandchild(p))
                self._recompute_height(self.left(p))
                self._recompute_height(self.right(p))
            self._recompute_height(p)
            if p._node._height == old_height:
                p = None #the while will note repeat
            else:
                p = self.parent(p) #repeat with parent

    # --------------------- overriding balancing hooks ---------------------

    def _rebalance_insert(self, p):
        """Call to indicate that position p is newly added."""
        self._rebalance(p)

    def _rebalance_delete(self, p):
        """Call to indicate that a child of p has been removed."""
        self._rebalance(p)


    # --------------------- OVERRIDING PARENT METHODS ---------------------

    # --------------------- public methods providing "positional" support ---------------------

    def first(self):
        """Return the first Position in the tree (or None if empty)."""
        return self._subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        """Return the last Position in the tree (or None if empty)."""
        return self._subtree_last_position(self.root()) if len(self) > 0 else None

    def find_position(self, k):
        """Return position with key k, or else neighbor (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)  # hook for balanced tree subclasses
            return p

    def delete(self, p):
        self._validate(p)                            # inherited from LinkedBinaryTree
        if self.left(p) and self.right(p):           # p has two children
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())    # from LinkedBinaryTree
            p =  replacement
        # now p has at most one child
        parent = self.parent(p)
        self._delete(p)                              # inherited from LinkedBinaryTree
        self._rebalance_delete(parent)

    # --------------------- public methods for (standard) map interface ---------------------

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                if p._node._afterpos is None:
                    p._node._beforepos._node._afterpos = None
                elif p._node._beforepos is None:
                    p._node._afterpos._node._beforepos = None
                else:
                    if self.left(p) and self.right(p):
                        p._node._afterpos._node._beforepos = p._node._beforepos
                        p._node._beforepos= p._node._beforepos._node._beforepos
                    else:
                        p._node._afterpos._node._beforepos = p._node._beforepos
                        p._node._beforepos._node._afterpos = p._node._afterpos
                self.delete(p)  # rely on positional version
                return  # successful deletion complete
            self._rebalance_access(p)  # hook for balanced tree subclasses
        raise KeyError('Key Error: ' + repr(k))

    def __iter__(self):
        """Generate an iteration of all keys in the map in order."""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def __setitem__(self, k, v):
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))  # from LinkedBinaryTree
        else:
            p = self.root()
            item = self._Item(k, v)
            node = self._Node(item)
            leaf=None
            while p is not None:
                if p.key() == k:
                    p.element()._value = v  # replace existing item's value
                    self._rebalance_access(p)  # hook for balanced tree subclasses
                    return
                elif p.key() < k:
                    if self.right(p) is None:
                        leaf = self._add_node_right(p, node)
                        p._node._afterpos = leaf
                        leaf._node._beforepos = self.parent(leaf)

                        # print("beaforefoglia", leaf._node._beforepos.key(), "foglia", leaf.key())
                        self._rebalance_insert(leaf)
                        p=self.right(p)
                    else:
                        if p._node._afterpos.key() > k:
                            p._node._afterpos = self._make_position(node)
                            p._node._afterpos._node._beforepos = p
                        p = self.right(p)
                else:
                    if self.left(p) is None:
                        leaf = self._add_node_left(p, node)
                        p._node._beforepos = leaf
                        leaf._node._afterpos = self.parent(leaf)
                        # print("afterfoglia", leaf._node._afterpos.key(), "foglia", leaf.key())
                        self._rebalance_insert(leaf)
                        p=self.left(p)
                    else:
                        if p._node._beforepos.key() < k:
                            p._node._beforepos = self._make_position(node)
                            p._node._beforepos._node._afterpos = p
                        p = self.left(p)
    # --------------------- public methods for sorted map interface ---------------------

    def __reversed__(self):
        """Generate an iteration of all keys in the map in reverse order."""
        p = self.last()
        while p is not None:
            yield p.key()
            p = self.before(p)

    def find_min(self):
        """Return (key,value) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_max(self):
        """Return (key,value) pair with maximum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.last()
            return (p.key(), p.value())

    def find_le(self, k):
        """Return (key,value) pair with greatest key less than or equal to k.
            
        Return None if there does not exist such a key.
        """
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if k < p.key():
                p = self.before(p)
            return (p.key(), p.value()) if p is not None else None

    def find_lt(self, k):
        """Return (key,value) pair with greatest key strictly less than k.
        
        Return None if there does not exist such a key.
        """
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if not p.key() < k:
                p = self.before(p)
            return (p.key(), p.value()) if p is not None else None

    def find_ge(self, k):
        """Return (key,value) pair with least key greater than or equal to k.
            
        Return None if there does not exist such a key.
        """
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)  # may not find exact match
            if p.key() < k:  # p's key is too small
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_gt(self, k):
        """Return (key,value) pair with least key strictly greater than k.
        
        Return None if there does not exist such a key.
        """
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if not k < p.key():
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        """Iterate all (key,value) pairs such that start <= key < stop.
            
        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                # we initialize p with logic similar to find_ge
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)


################TEST#######################
print("##########---TEST MYAVLTREEMAP---###########")
t1 = MyAVLTreeMap()
chiavi = [5,2,12,1,3,15,8,7,11,10,9]
for i in range(len(chiavi)):
    t1.__setitem__(chiavi[i],i*i)


for k in t1.inorder():
    p = t1.find_position(k.key())
    resultafter = t1.after(p)
    resultbefore = t1.before(p)
    if resultafter == None:
        print("result before", resultbefore.key(), "Position", p.key(), "result after", resultafter)
    elif resultbefore == None:
        print("result before", resultbefore, "Position", p.key(), "result after", resultafter.key())
    else:
        print("result before", resultbefore.key(), "Position", p.key(), "result after", resultafter.key())


for k in t1.preorder():
    print(k.key(), end=" ")
print("\n")

print("--Test AvlTreeMap delitem--")
t1.__delitem__(9)
print("delete 9")
p1=t1.find_position(10)
p2=t1.find_position(8)
for k in t1.preorder():
    print(k.key(), end=" ")
print("\n")

resultafter = t1.after(p1)
resultbefore = t1.before(p1)
if resultafter == None:
    print("result before", resultbefore.key(), "Position", p1.key(), "result after", resultafter)
elif resultbefore == None:
    print("result before", resultbefore, "Position", p1.key(), "result after", resultafter.key())
else:
    print("result before", resultbefore.key(), "Position", p1.key(), "result after", resultafter.key())

resultafter = t1.after(p2)
resultbefore = t1.before(p2)
if resultafter == None:
    print("result before", resultbefore.key(), "Position", p2.key(), "result after", resultafter)
elif resultbefore == None:
    print("result before", resultbefore, "Position", p2.key(), "result after", resultafter.key())
else:
    print("result before", resultbefore.key(), "Position", p2.key(), "result after", resultafter.key())

print("--Test First Avl--")
print(t1.first().key())
print("-- Test last avl--")
print(t1.last().key())
print("--Test Iter Avl--")
for i in t1:
    print(i , end=" ")

print("\n-- Test Reversed AVL --")
for i in t1.__reversed__():
    print(i, end=" ")
print("\n--Test find min AVL--")
print("key: ", t1.find_min()[0], "value: ", t1.find_min()[1])
print("--Test find max AVL--")
print("key: ", t1.find_max()[0], "value: ", t1.find_max()[1])
print("--Test find le AVL--")
print("key: ", t1.find_le(8)[0], "value: ", t1.find_le(8)[1])
print("--Test find lt AVL--")
print("key: ", t1.find_lt(8)[0], "value: ", t1.find_lt(8)[1])
print("--Test find ge AVL--")
print("key: ", t1.find_ge(8)[0], "value: ", t1.find_ge(8)[1])
print("--Test find gt AVL--")
print("key: ", t1.find_gt(8)[0], "value: ", t1.find_gt(8)[1])
print("--Test find range AVL--")
for item in t1.find_range(3,12):
    print("key: ", item[0], "value: ", item[1])