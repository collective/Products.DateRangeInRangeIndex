from AccessControl import ClassSecurityInfo
from Globals import (
    DTMLFile, 
    InitializeClass,
)
from BTrees.IIBTree import (
    multiunion, 
    intersection, 
    IISet
)
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.ZCatalog.Catalog import Catalog
from Products.PluginIndexes.common.util import parseIndexRequest
from Products.PluginIndexes.common.UnIndex import UnIndex
from .interfaces import IDateRangeInRangeIndex
from zope.interface import implementer

_marker = list()

VIEW_PERMISSION = 'View'
MGMT_PERMISSION = 'Manage ZCatalogIndex Entries'

manage_addDRIRIndexForm = DTMLFile('www/addDRIRIndex', globals())

def manage_addDRIRIndex(self, id, extra=None, REQUEST=None, RESPONSE=None,
                         URL3=None):
    """Adds a date range in range index"""
    result = self.manage_addIndex(id, 'DateRangeInRangeIndex', extra=extra,
                                  REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)
    return result    

@implementer(IDateRangeInRangeIndex)
class DateRangeInRangeIndex(UnIndex):
    """
    """
    __implements__ = (getattr(UnIndex,'__implements__',()),)

    meta_type="DateRangeInRangeIndex"
    security = ClassSecurityInfo()
    manage_options= (
        {'label': 'Settings',
         'action': 'manage_main',
        },
    )
    manage_main = PageTemplateFile('www/manageDRIRIndex', globals())    
    query_options = ['start', 'end']
    
    startindex = endindex = None
    
    def __init__(self, id, ignore_ex=None, call_methods=None, 
                 extra=None, caller=None):
        UnIndex.__init__(self, id, ignore_ex=None, call_methods=None, 
                         extra=None, caller=None)
        self.caller = caller
	if extra is None:
            return        
        try:
            self.startindex = extra.startindex
            self.endindex   = extra.endindex
        except AttributeError:
            try:
                # alternative: allow a dict (lowers bootstrapping effort 
                # from code)
                self.startindex = extra['startindex']
                self.endindex   = extra['endindex']
            except AttributeError:
                raise ValueError, "DateRangeInRangeIndex needs 'extra' kwarg "+\
                      "with keys or attributes 'startindex' and 'endindex' " +\
                      "pointing to two existing DateIndex'es."
        
        
    def _getCatalog(self):
        # attention: we're using heuristics here
        if hasattr(self.caller, 'uids') or isinstance(self.caller, Catalog):
            return self.caller
        elif hasattr(self.caller, '_catalog'):
            return self.caller._catalog        
        else:
            raise 'DateRangeInRangeIndex cant work w/o knowing about its catalog'


    def _apply_index(self, request, cid='', type=type):
        """Apply the index to query parameters given in the request arg.

        The request argument should be a mapping object.

        If the request does not have a key which matches the "id" of
        the index instance, then None is returned.

        If the request *does* have a key which matches the "id" of
        the index instance, one of a few things can happen:

          - if the value is a blank string, None is returned (in
            order to support requests from web forms where
            you can't tell a blank string from empty).

          - if the value is a nonblank string, turn the value into
            a single-element sequence, and proceed.

          - if the value is a sequence, return a union search.

        """
        record = parseIndexRequest(request, self.id, self.query_options)        
        if record.keys is None: 
            return None

        q_start = record.get('start', None)
        q_end = record.get('end', None)        
        
        if q_start is None or q_end is None:
            return IISet(), (self.id,)
            
        # get both indexes: for start and end
        zcatalog = self._getCatalog()
        i_start = zcatalog.getIndex(self.startindex)
        i_end   = zcatalog.getIndex(self.endindex)
        
        # search:
        #        
        #       q_start|--------------------|q_end
        #
        # 1) i_start|---------------------------|i_end
        #
        # 2) i_start|---------------|i_end
        # 
        # 3)           i_start|-----------------|i_end
        #
        # 4)           i_start|-----|i_end

        ###################################
        # do 1) objects with "both outside"
        #        
        query1_1 = {self.startindex: {
            # objects starting before q_start
            'query': q_start,
            'range': 'max',
            }
        }
        res1_1 = i_start._apply_index(query1_1)

        query1_2 = {self.endindex: {
            # objects ending after q_end
            'query': q_end,
            'range': 'min',
            }
        }
        res1_2 = i_end._apply_index(query1_2)
        res1 = intersection(res1_1[0], res1_2[0])

        #####################################
        # do 2) objects with "start inside"
        # 
        query2_1 = {self.endindex: {
            # objects ending after q_start
            'query': q_start,
            'range': 'min',
            }
        }
        res2_1 = i_end._apply_index(query2_1)

        query2_2 = {self.endindex: {
            # objects ending before q_end
            'query': q_end,
            'range': 'max',
            }
        }
        res2_2 = i_end._apply_index(query2_2)
        res2 = intersection(res2_1[0], res2_2[0])

        ###################################
        # do 3) objects with "end inside"
        query3_1 = {self.startindex: {
            # objects starting after q_start
            'query': q_start,
            'range': 'min',
            }
        }
        res3_1 = i_start._apply_index(query3_1)

        query3_2 = {self.startindex: {
            # objects starting before q_end
            'query': q_end,
            'range': 'max',
            }
        }
        res3_2 = i_start._apply_index(query3_2)
        res3 = intersection(res3_1[0], res3_2[0])

        ###################################
        # do 4) object where both are inside
        # -> already found with 2) and 3)  :-)


        ###################################
        # union the three results
        result = multiunion([res1, res2, res3])

        # last: return the result
        return result, (self.id,)

    def index_object(self, documentId, obj, threshold=None):
        """not used, we're just a kind of proxy without own storage"""
        return 0
    
    def unindex_object(self, documentId):
        """ In this index we need to do exact nothing, as it is just a proxy
        """      
        pass
        
    security.declareProtected(VIEW_PERMISSION, 'getStartIndexField')
    def getStartIndexField(self):
        return self.startindex

    security.declareProtected(VIEW_PERMISSION, 'getEndIndexField')
    def getEndIndexField(self):
        return self.endindex

        
InitializeClass(DateRangeInRangeIndex)
