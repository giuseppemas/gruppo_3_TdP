from TdP_collections.map.avl_tree import AVLTreeMap
from TdP_collections.map.red_black_tree import RedBlackTreeMap
import random
import time

from TdP_collections.map.binary_search_tree import TreeMap

''' Entrambe le classi vengono estese per inserire al loro interno un parametro conteggio, che tiene traccia di quante
    volte una _subtree_search viene richiamata durante una ricerca e quindi quanti confronti vengono sostanzialmente eseguiti'''
class MyAVLTreeMap(AVLTreeMap):
    conteggio = 0

    def _subtree_search(self, p, k):
        self.conteggio += 1
        """Return Position of p's subtree having key k, or last node searched."""
        if k == p.key():  # found match
            return p
        elif k < p.key():  # search left subtree
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:  # search right subtree
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p

    def reset_conteggio(self):
        self.conteggio = 0

    def get_conteggio(self):
        return self.conteggio

class MyRedBlackTreeMap(RedBlackTreeMap):
    conteggio = 0

    def _subtree_search(self, p, k):
        self.conteggio += 1
        """Return Position of p's subtree having key k, or last node searched."""
        if k == p.key():  # found match
            return p
        elif k < p.key():  # search left subtree
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:  # search right subtree
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p

    def reset_conteggio(self):
        self.conteggio = 0

    def get_conteggio(self):
        return self.conteggio

'''Si sceglie di inserire in modo sequenziale i primi N numeri in entrambi gli alberi, e di fare R ricerche a caso
    su entrambi gli alberi, cercando ogni volta la stessa coppia di chiave, alla fine si farà una media e si può vedere 
    che l'AVL è più efficiente del RB, per la legge dei grandi numeri si consiglia di scegliere un R molto grande, R=10000 
    è sufficiente per vedere risultati solidi'''

rb = MyRedBlackTreeMap()
avl = MyAVLTreeMap()
R = 10000 # numero di ricerche da effettuare
N = 1000  # numero di elementi inseriti negli alberi
d = 50  # Rate di disordine, ogni quanti inserimenti ordinati uno è random ?
range_d = 10000 # I numeri casuali da inserire ogni d inserimenti sarà pescato dall'intervallo(N,N+range_d)

tot_rb = 0
tot_avl = 0
print("\nEFFICIENZA SULl'INSERIMENTO ORDINATO:")
for i in range(N):
    rb.__setitem__(i,i)
    avl.__setitem__(i,i)
    #print("key:", i, i, "--> Search AVL:", avl.get_conteggio(), "Search RB:", rb.get_conteggio())
    tot_avl += avl.get_conteggio()
    tot_rb += rb.get_conteggio()
    rb.reset_conteggio()
    avl.reset_conteggio()

print("\nSu un totale di",N,"inserimenti queste sono le search richiamate mediamente "
                          "dai due alberi per inserire le stesse chiavi:","\nNumero medio di search per AVL:"
                                                  "",tot_avl/N,"\nNumero medio di search per RB:", tot_rb/N)

avl.reset_conteggio()
rb.reset_conteggio()

tot_rb = 0
tot_avl = 0
print("\nEFFICIENZA SULLA RICERCA:")
for k in range(R):
    chiave = random.randint(1,N-1)
    avl_chiave = avl[chiave]
    rb_chiave = rb[chiave]
    #print("key:",avl_chiave, rb_chiave,"--> Search AVL:",avl.get_conteggio(),"Search RB:",rb.get_conteggio())
    tot_avl += avl.get_conteggio()
    tot_rb += rb.get_conteggio()
    rb.reset_conteggio()
    avl.reset_conteggio()

print("\nSu un totale di",R,"simulazioni queste sono le search richiamate mediamente "
                          "dai due alberi per trovare le stesse chiavi con elementi"
                          " nello stesso ordine:","\nNumero medio di search per AVL:"
                                                  "",tot_avl/R,"\nNumero medio di search per RB:", tot_rb/R)

avl.reset_conteggio()
rb.reset_conteggio()
tot_rb = 0
tot_avl = 0
print("\nEFFICIENZA SULl'INSERIMENTO QUASI ORDINATO:")
for i in range(N):
    if i%d == 0:
        x = random.randint(N,N+range_d)
        rb.__setitem__(x, x)
        avl.__setitem__(x, x)
        #print("key:", x, x, "--> Search AVL:", avl.get_conteggio(), "Search RB:", rb.get_conteggio())
        tot_avl += avl.get_conteggio()
        tot_rb += rb.get_conteggio()
        rb.reset_conteggio()
        avl.reset_conteggio()
    else:
        rb.__setitem__(i, i)
        avl.__setitem__(i, i)
        #print("key:", i, i, "--> Search AVL:", avl.get_conteggio(), "Search RB:", rb.get_conteggio())
        tot_avl += avl.get_conteggio()
        tot_rb += rb.get_conteggio()
        rb.reset_conteggio()
        avl.reset_conteggio()

print("\nSu un totale di",N,"inserimenti QUASI ORDINATI queste sono le search richiamate mediamente "
                          "dai due alberi per inserire le stesse chiavi:","\nNumero medio di search per AVL:"
                                                  "",tot_avl/N,"\nNumero medio di search per RB:", tot_rb/N)




print("\nEFFICIENZA SULl'INSERIMENTO ORDINATO IN SECONDI:")
avl = MyAVLTreeMap()
rb = MyRedBlackTreeMap()

inizio_avl = time.clock()
for i in range(N):
    avl.__setitem__(i,i)
fine_avl = time.clock()
t_avl = fine_avl-inizio_avl

inizio_rb = time.clock()
for i in range(N):
    rb.__setitem__(i,i)
fine_rb = time.clock()
t_rb = fine_rb-inizio_rb

print(N,"inserimenti:","\nTempo AVL:",t_avl,"\nTempo RB:", t_rb)

print("\nEFFICIENZA SULl'INSERIMENTO QUASI ORDINATO IN SECONDI:")
avl = MyAVLTreeMap()
rb = MyRedBlackTreeMap()

x = list()

for i in range(N):
    if i%d == 0:
        x.append(random.randint(N,N+range_d))
    else:
        x.append(i)

inizio_avl = time.clock()
for i in range(N):
    avl.__setitem__(x[i],x[i])

fine_avl = time.clock()
t_avl = fine_avl-inizio_avl

inizio_rb = time.clock()
for i in range(N):
        rb.__setitem__(x[i], x[i])

fine_rb = time.clock()
t_rb = fine_rb-inizio_rb

print(N,"inserimenti QUASI ORDINATI:","\nTempo AVL:",t_avl,"\nTempo RB:", t_rb)