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
        pass
    
    def fusion(self, T1):
        """
            Il metodo fusion(T1), invocato sul MyRBTreeMap T, prende in input un RBTreeMap T1,
            le cui chiavi sono tutte maggiori delle chiavi presenti in T e inserisce in T tutte le chiavi di T1.
            Nel caso in cui esista una chiave di T1 minore di una chiave in T,
            il metodo deve lanciare un’eccezione ValueError.
            (Domanda bonus 3 punti extra: fornire un’implementazione di fusion() con complessità di tempo di
            O( log n + log m), dove n sono le chiavi dell’albero T e m sono le chiavi dell’albero T1).
            """
    pass
