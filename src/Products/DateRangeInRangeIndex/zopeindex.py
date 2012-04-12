from  persistent import Persistent
from BTrees.IFBTree import (
    multiunion,
    intersection,
)
from zope.interface import implements
from zope.container.contained import Contained
from zope.index.interfaces import IIndexSearch, IIndexSort
from zope.catalog.interfaces import ICatalogIndex

class DateRangeInRangeIndex(Persistent, Contained):

    implements(
        ICatalogIndex,
        IIndexSort,
    )

    def __init__(self, i_start_id, i_end_id):
        self._i_start_id = i_start_id
        self._i_end_id = i_end_id

    @property
    def _i_start(self):
        return self.__parent__[self._i_start_id]

    @property
    def _i_end(self):
        return self.__parent__[self._i_end_id]

    def index_doc(self, docid, value):
        """ ICatalogIndex: zope.index.interfaces.IInjection
        
        we dont need this, but we need the stubs.
        """
        pass

    def unindex_doc(self, docid):
        pass

    def clear(self):
        pass

    def sort(self, docids, reverse=False, limit=None):
        """zope.catalog.interfaces.IIndexSort"""
        return self._i_start.sort(docids, reverse, limit)

    def apply(self, query):
        """see IIndexSearch.apply
        
        expected query is a 2-tuple with datetime.datetime 

        Use case as following:
        
        search:
                
             q_start|--------------------|q_end
        
        cases:
        
        1) i_start|---------------------------|i_end
        
        2) i_start|---------------|i_end
         
        3)           i_start|-----------------|i_end
        
        4)           i_start|-----|i_end
        """
        if len(query) != 2 or not isinstance(query, tuple):
            raise TypeError("two-length tuple expected", query)
        q_start, q_end = query

        ###################################
        # do 1) objects with "both outside"
        #   

        # objects starting before q_start     
        query1_1 = (None, q_start)
        res1_1 = self._i_start.apply(query1_1)

        # objects ending after q_end
        query1_2 = (q_end, None)
        res1_2 = self._i_end.apply(query1_2)

        res1 = intersection(res1_1, res1_2)

        #####################################
        # do 2) objects with "start inside"
        #
        query2 = (q_start, q_end)
        res2 = self._i_start.apply(query2)

        ###################################
        # do 3) objects with "end inside"
        query3 = (q_start, q_end)
        res3 = self._i_end.apply(query3)


        ###################################
        # do 4) object where both are inside
        # -> already found with 2) and 3)  :-)


        ###################################
        # union the three results
        result = multiunion([res1, res2, res3])

        return result
