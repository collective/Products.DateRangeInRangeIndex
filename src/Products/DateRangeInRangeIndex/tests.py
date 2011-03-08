import unittest
import doctest
from interlude import interact
from Testing import ZopeTestCase as ztc
from Products.ZCatalog.Catalog import Catalog
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex
from Products.DateRangeInRangeIndex.index import DateRangeInRangeIndex
from DateTime import DateTime

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

ztc.installProduct('DateRangeInRangeIndex')

class DummyEvent(object):
    """some dummy with a start and end to index"""
    
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end        

class DRIRITestcase(ztc.ZopeTestCase):
    """Base TestCase for DateRangeInRangeIndex."""
    
    def afterSetUp(self):
        """set up a base scenario"""
        self.app.catalog = Catalog()
        idxstart = DateIndex('start')
        idxend   = DateIndex('end')
        self.app.catalog.addIndex('start', idxstart)
        self.app.catalog.addIndex('end',   idxend)
        driri = DateRangeInRangeIndex('driri', 
                                      extra={'startindex':'start',
                                             'endindex':'end'},
                                      caller=self.app.catalog)
        self.app.catalog.addIndex('driri', driri)
        self.app.catalog.addColumn('id')
        
    def buildDummies(self, cases):
        """setup dummies"""
        dummies = {}
        for id in cases:
            dummy = DummyEvent(id, DateTime(cases[id][0]), 
                                   DateTime(cases[id][1]))
            dummies[id] = dummy
        return dummies
    
    def catalogDummies(self, dummies):
        for id in dummies:
            self.app.catalog.catalogObject(dummies[id], id)    

    def idsOfBrainsSorted(self, brains):
        return sorted([brain.id for brain in brains])

TESTFILES = ['index.txt',]

def test_suite():

    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact,
                },
            test_class=DRIRITestcase
        ) for filename in TESTFILES])