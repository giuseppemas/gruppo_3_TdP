from pkg_2.MyTreeMap import MyTreeMap

'''
Implementare il metodo LCA(p, q) della classe MyTreeMap che, prese in input due position p e q, restituisce la position
dell’antenato comune dei nodi identificati da p e q che si trova al livello più grande nell’albero.
Il metodo LCA() deve avere complessità di tempo O(h), dove h è l’altezza dell’albero.
'''

class MyTreeMap_LCA(MyTreeMap):

    def LCA(self, p, q):

        nodep = self._validate(p)
        nodeq = self._validate(q)
        current = self._root

        while current is not None:
            if nodep._element._key > current._element._key and nodeq._element._key > current._element._key:
                current = current._right
            elif nodep._element._key < current._element._key and nodeq._element._key < current._element._key:
                current = current._left
            else:
                return self._make_position(current)




print("Test di LCA:\n")
t = MyTreeMap_LCA()
chiavi = [10,12,5,4,20,8,7,15,13]
for i in range(9):
    t.__setitem__(chiavi[i],i*i)

# Rappresentazione dell'albero su cui faremo i test:
#
#                    10
#                 /     \
#                /       \
#               5        12
#             /  \         \
#            4    8         20
#                /         /
#               7         15
#                        /
#                       13

# Salvo le position dell'albero in una lista
pos = list()
for item in t.positions():
    pos.append(item)
'''
pos[ 0 ]= 4
pos[ 1 ]= 5
pos[ 2 ]= 7
pos[ 3 ]= 8
pos[ 4 ]= 10
pos[ 5 ]= 12
pos[ 6 ]= 13
pos[ 7 ]= 15
pos[ 8 ]= 20
'''

print("LCA di", pos[1].key(),"e", pos[4].key()," --->", t.LCA(pos[1], pos[4]).key())
print("LCA di", pos[2].key(),"e", pos[6].key()," --->", t.LCA(pos[2], pos[6]).key())
print("LCA di", pos[0].key(),"e", pos[3].key()," --->", t.LCA(pos[0], pos[3]).key())
print("LCA di", pos[1].key(),"e", pos[1].key()," --->", t.LCA(pos[1], pos[1]).key())  # Stessa position
print("LCA di", pos[3].key(),"e", pos[7].key()," --->", t.LCA(pos[3], pos[7]).key())
print("LCA di", pos[5].key(),"e", pos[8].key()," --->", t.LCA(pos[5], pos[8]).key())  # Padre e figlio

# Nodi di alberi diversi

t2 = MyTreeMap_LCA()
t2.__setitem__(1,1)
pos2 = t2.root()
try:
    print("LCA di", pos2.key(), "e", pos[7].key(), " --->", t.LCA(pos2, pos[7]).key())
except Exception as e:
    print("Error: ",e)