from TdP_collections.map.red_black_tree import RedBlackTreeMap

'''
Progettare la classe MyRBTreeMap che estende RBTreeMap aggiungendo due metodi: split() e fusion().
'''

class MyRedBlackTreeMap(RedBlackTreeMap):

    def split(self, k):
        """
            Il metodo split(k), invocato sul MyRBTreeMap T, prende in input una chiave k e
            restituisce due MyRBTreeMap T1 e T2 contenenti, rispettivamente, tutte le chiavi di T minori di k
            e tutte le chiavi di T maggiori di k (la chiave k viene eliminata).
            Il metodo deve avere complessità O(log n), dove n è il numero delle chiavi di T.
            N.B. Il metodo split distrugge l’albero t originario.
            """
        T1= MyRedBlackTreeMap()
        T2 = MyRedBlackTreeMap()
        walk = self.root()
        ultimateT1 = None
        ultimateT2 = None
        #if root is equal to k
        if walk.key() == k:
            T1._root = self.left(walk)._node
            T2._root = self.right(walk)._node
            T1._root._red = False
            T2._root._red = False
            return T1,T2
        #go right
        elif walk.key() < k:
            #info = self.min_blackdep(walk)
            #blackD_T1 = info[1]
            #blackD_T2 = 0
            T1._root = walk._node
            T1._root._red = False
            walk = self.right(walk)
            ultimateT1 = T1.root()
            T1._size=1
            print("T1 root: ", T1.root().key(), walk.key())
            while walk.key() != k:
                if walk is None:
                    raise KeyError("key value is not in Tree")
                else:
                    if walk.key() < k:
                        #go right
                        if walk._node._parent != ultimateT1._node:
                            walk._node._parent = ultimateT1._node
                            ultimateT1._node._right = walk._node
                        walk = self.right(walk)
                        ultimateT1 = walk
                        print("T1 root - walk: ", T1.root().key(), walk.key())
                    else:
                        #we need to cut the trees before going left
                        if T2._root is None:
                            T2._root = walk._node
                            print("T2 root: ", T2.root().key())
                            T2._root._red = False
                            ultimateT2 = T2.root()
                            #blackD_T2 = T2.max_blackdep(ultimateT2)[1]
                            T2._size =1
                        else:
                            ultimateT2 = walk
                        walk = self.left(walk)
                        print("T2 nodo right, left: ", walk.key(), T2.right(T2.root()).key(), T2.left(T2.root()).key())

        else: #go left k< walk.key()
            #info = self.max_blackdep(walk)
            #blackD_T2 = info[1]
            T2._root = walk._node
            T2._root._red = False
            walk = self.left(walk)
            ultimateT2 = T2.root()
            T2._size = 1
            while walk.key() != k:
                if walk is None:
                    raise KeyError("key value is not in Tree")
                else:
                    if k < walk.key():
                        # go left
                        if walk._node._parent != ultimateT2._node:
                            walk._node._parent = ultimateT2._node
                            ultimateT2._node._left = walk._node
                        walk = self.left(walk)
                        ultimateT2 = walk
                    else:
                        # we need to cut the trees before going right
                        if T1._root is None:
                            T1._root = walk._node
                            T1._root._red = False
                            ultimateT1 = T1.root()
                            T1._size = 1
                        else:
                            ultimateT1 = walk
                        walk = self.right(walk)

        print("FINE WHILE\n")

        if self.right(walk) is not None:
            if not self._is_red(walk):
                walk._node._right._red = False
            if T2.root() is None:
                T2._root = walk._node._right
                T2._root._red = False
                T2._size = 1
            else:
                ultimateT2._node._left = walk._node._right #NON ASSEGNAMO LA T2.root
                walk._node._right._parent = ultimateT2._node
            #print("T1 nodo right, left: ", walk.key(), T1.right(T1.root()).key(), T1.left(T1.root()).key())
            #print("T2 nodo right, left: ", walk.key(), T2.right(T2.root()).key(), T2.left(T2.root()).key())
        else:
            ultimateT2._node._left = None
            #print("T1 nodo right, left: ", walk.key(), T1.right(T1.root()).key(), T1.left(T1.root()).key())
            #print("T2 nodo right, left: ", walk.key(), T2.right(T2.root()).key(), T2.left(T2.root()).key())

        if self.left(walk) is not None:
            if not self._is_red(walk):
                walk._node._left._red = False
            if T1.root() is None:
                T1._root = walk._node._left
                T1._root._red = False
                T2._size = 1
            else:
                ultimateT1._node._right = walk._node._left
                walk._node._left._parent = ultimateT1._node
            #print("T1 nodo right, left: ", walk.key(), T1.right(T1.root()).key(), T1.left(T1.root()).key())
            #print("T2 nodo right, left: ", walk.key(), T2.right(T2.root()).key(), T2.left(T2.root()).key())
        else:
            ultimateT1._node._right = None
        # delete Key
        walk._node._parent = None
        walk._node._left = None
        walk._node._right = None
        return T1,T2


    def min_blackdep(self,p):
        """Return a min value of tree and blackDepth of root"""
        blackdepth = 0
        walk = p
        while walk is not None:  # keep walking left
            if not self._is_red(walk):
                blackdepth+=1
            if self.left(walk) is not None:
                walk = self.left(walk)
            else:
                break
        return walk,blackdepth


    def max_blackdep(self,p):
        """Return a max value of tree and blackDepth of root"""
        blackdepth = 0
        walk = p
        while walk  is not None:  # keep walking left
            if not self._is_red(walk):
                blackdepth+=1
            if self.right(walk) is not None:
                walk = self.right(walk)
            else:
                break
        return walk,blackdepth


    def _concatene(self, p, t1, t2):
        """Attach trees t1 and t2, respectively, as the left and right subtrees of the external Position p.
        Raise TypeError if trees t1 and t2 do not match type of this alberi.
        Raise ValueError if Position p is invalid or not external.
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):  # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():# attached t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = p._node # set t1 to new root
        if not t2.is_empty():  # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None  # set t2 instance to empty
            t2._size = 0


    def fusion(self, T1):
        """
            Il metodo fusion(T1), invocato sul MyRBTreeMap T, prende in input un RBTreeMap T1,
            le cui chiavi sono tutte maggiori delle chiavi presenti in T e inserisce in T tutte le chiavi di T1.
            Nel caso in cui esista una chiave di T1 minore di una chiave in T,
            il metodo deve lanciare un’eccezione ValueError.
            (Domanda bonus 3 punti extra: fornire un’implementazione di fusion() con complessità di tempo di
            O( log n + log m), dove n sono le chiavi dell’albero T e m sono le chiavi dell’albero T1).
            """
        T_info = self.max_blackdep(self.root())
        T1_info = T1.min_blackdep(T1.root())

        if T1_info[0].key()<T_info[0].key():
            raise ValueError("The argument contains a key less than a key of self")
        else:

            print(T_info[1], T1_info[1])
            diffBD = T_info[1] - T1_info[1]
            print("diff", diffBD,"black self", T_info[1],"black arg", T1_info[1])
            if diffBD == 0:
                pos = self._make_position(self._Node(T1_info[0]._node._element))
                pos._node._red = False
                T1.delete(T1_info[0])
                self._concatene(pos, self, T1)
            elif diffBD > 0:
                black = T_info[1]
                walk = self.root()
                while walk is not None:
                    if black==T1_info[1]:
                        break
                    else:
                        walk = self.right(walk)
                    if not self._is_red(walk):
                        black-=1

                    print(black, walk.key(), "<--- blackdepth and root T")
                print("print <0",walk.key(), "key attach", black)
                pos = self._make_position(self._Node(T1_info[0]._node._element))
                pos._node._red = False
                T1.delete(T1_info[0])
                self._concat(pos,walk,T1, True)
            else:
                black = T1_info[1]
                walk = T1.root()
                print(walk.key())
                while walk is not None:
                    if black == T_info[1]:
                        break
                    else:
                        walk = T1.left(walk)
                    if not T1._is_red(walk):
                        black-=1
                print(walk.key(), "key attach")
                pos = T1._make_position(T1._Node(T_info[0]._node._element))
                pos._node._red = False
                self.delete(T_info[0])
                T1._concat(pos,walk,self, False)


    def _concat(self, p, nodeattach, subtree, boolean):
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(subtree):  # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(subtree)
        parent = self.parent(nodeattach)
        node._parent = parent._node
        nodeattach._node._parent = node
        if boolean:
            parent._node._right = node
            node._left = nodeattach._node
            if not subtree.is_empty():
                subtree._root._parent = node
                node._right = subtree._root
                subtree._root = None
        else:
            parent._node._left = node
            node._right = nodeattach._node
            if not subtree.is_empty():
                subtree._root._parent = node
                node._left = subtree._root
                subtree._root = None


# ----SPLIT----

def color(T1, p):
    color = ""
    if T1._is_red(p):
        color = "RED"
    else:
        color = "BLACK"
    return color
print("--------------TEST SPLIT------------------")
print("Test Split\n")
rbt1 = MyRedBlackTreeMap()
rbt2 = MyRedBlackTreeMap()
chiaveSplit1 = [8, 5, 20, 4, 6, 11, 25, 10, 12] # k = 11
chiaveSplit2 = [22, 19, 30, 11, 21, 31, 7, 16, 20] # k = 20

for i in range(len(chiaveSplit1)):
    rbt1.__setitem__(chiaveSplit1[i],i*i)

for i in rbt1.preorder():
    print(i.key(), color(rbt1,i), end=" ")

print("\n")

T1,T2 = rbt1.split(20)

for i in T1.preorder():
    print(i.key(), color(T1,i))
print("\n")
for k in T2.preorder():
    print(k.key(), color(T2,k))


print("Test Split 2 \n")

for i in range(len(chiaveSplit2)):
    rbt2.__setitem__(chiaveSplit2[i],i+i)

for i in rbt2.preorder():
    print(i.key(), end=" ")
print("\n")

T1,T2 = rbt2.split(20)

for i in T1.preorder():
    print(i.key(),color(T1,i))
print("\n")
for k in T2.preorder():
    print(k.key(),color(T2,k))




# ----FUSION----
print("---------------FUSION--------------")
t0 = MyRedBlackTreeMap()
t1 = MyRedBlackTreeMap()
t2 = MyRedBlackTreeMap()
t3 = MyRedBlackTreeMap()
t4 = MyRedBlackTreeMap()
t5 = MyRedBlackTreeMap()

chiavi = [5,2,12,1,3,15,8,7,11]
chiavi0 = [30,22,35,17,26]
chiavi2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
chiavi3 = [30,22,35,17,26]
chiavi4 = [1,2,3,4,5]
chiavi5 = [20,21,22,23,24,25,26,27,28,29,30]

for i in range(len(chiavi)):
    t0.__setitem__(chiavi[i],i*i)

for i in range(len(chiavi0)):
    t3.__setitem__(chiavi0[i],i+i)

for i in range(len(chiavi3)):
    t1.__setitem__(chiavi3[i], i+i)

for l in range(len(chiavi2)):
    t2.__setitem__(chiavi2[l], i*i)

for i in range(len(chiavi4)):
    t4.__setitem__(chiavi4[i],i*i)

for i in range(len(chiavi5)):
    t5.__setitem__(chiavi5[i],i*i)

print("t0\n")
for i in t0.inorder():
    print(i.key(), color(t0,i))
print("\nt3\n")
for i in t3.inorder():
    print(i.key() ,color(t3,i))

print("-------TEST t0.FUSION(t3)------")
t0.fusion(t3)
print("t0")
for j in t0.inorder():
    print(j.key(),color(t0,j))
print("\n")

print("-------TEST t2.FUSION(t1)------")
t2.fusion(t1)
print("t2")
for j in t2.inorder():
    print(j.key(),color(t2,j))
print("\n")


print("t4")
for i in t4.inorder():
    print(i.key(), color(t4,i))
print("\nt5\n")
for i in t5.inorder():
    print(i.key() ,color(t5,i))
print("-------TEST t4.FUSION(t5)------")
t4.fusion(t5)
print("t5")
for l in t5.inorder():
    print(l.key(), color(t5,l))
print("\n")