from pkg_2.MyTreeMap import MyTreeMap
from TdP_collections.map.binary_search_tree import LinkedBinaryTree

'''
Implementare il metodo LCA(p, q) della classe MyTreeMap che, prese in input due position p e q, restituisce la position
dell’antenato comune dei nodi identificati da p e q che si trova al livello più grande nell’albero.
Il metodo LCA() deve avere complessità di tempo O(h), dove h è l’altezza dell’albero.
'''

class MyTreeMap_LCA(MyTreeMap):

    def LCA(self, p, q):
        if p == q:
            return p

        if p.is_root():
            return MyTreeMap_LCA(p,q.parent())
        elif q.is_root():
            return MyTreeMap_LCA(p.parent(), q)
        else:
            return MyTreeMap_LCA(p.parent(), q.parent())


print("Prova mia con positions.")

