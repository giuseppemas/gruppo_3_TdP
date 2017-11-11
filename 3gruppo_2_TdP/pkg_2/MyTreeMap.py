from TdP_collections.map.binary_search_tree import TreeMap

'''
Progettare la classe MyTreeMap che espone la stessa interfaccia di TreeMap ma implementa i metodi after() e before() con
complessità di tempo O(1), senza aumentare la complessità di tempo di tutti gli altri metodi.
'''

class MyTreeMap(TreeMap):
    
    def after(self, p):
        pass
    
    def before(self, p):
        pass

    def __str__(self):
        s = ''
        for i in self:
            s += str(i)
            s += '  '

        return s