import unittest
import doctest
from interlude import interact
from Testing import ZopeTestCase as ztc
from zope.catalog.catalog import Catalog as z3Catalog
from zope.catalog.field import FieldIndex
from Products.ZCatalog.Catalog import Catalog as z2Catalog
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex
from Products.DateRangeInRangeIndex.index import \
    DateRangeInRangeIndex as z2DateRangeInRangeIndex
from Products.DateRangeInRangeIndex.zopeindex import \
    DateRangeInRangeIndex as z3DateRangeInRangeIndex
import datetime
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

    dtfactory = None

    def afterSetUp(self):
        """set up a base scenario"""

        # Zope 2 Index bootstrap
        self.app.catalog = z2Catalog()
        idxstart = DateIndex('start')
        idxend = DateIndex('end')
        self.app.catalog.addIndex('start', idxstart)
        self.app.catalog.addIndex('end', idxend)
        driri = z2DateRangeInRangeIndex('driri',
                                      extra={'startindex':'start',
                                             'endindex':'end'},
                                      caller=self.app.catalog)
        self.app.catalog.addIndex('driri', driri)
        self.app.catalog.addColumn('id')

        # Zope 3 Index bootstrap
        self.app.z3catalog = z3Catalog()
        self.app.z3catalog[u'start'] = FieldIndex(field_name='start',
                                                  field_callable=False)
        self.app.z3catalog[u'end'] = FieldIndex(field_name='end',
                                                field_callable=False)
        self.app.z3catalog[u'driri'] = z3DateRangeInRangeIndex(u'start', u'end')


    def buildDummies(self, cases):
        """setup dummies"""
        dummies = {}
        for id in cases:
            dummy = DummyEvent(id, self.dtfactory(cases[id][0]),
                                   self.dtfactory(cases[id][1]))
            dummies[id] = dummy
        return dummies

    def catalogDummies(self, dummies):
        for id in dummies:
            self.app.catalog.catalogObject(dummies[id], id)

    def z3catalogDummies(self, dummies):
        for id in dummies:
            self.app.z3catalog.index_doc(id, dummies[id])

    def idsOfBrainsSorted(self, brains):
        return sorted([brain.id for brain in brains])


    def idsOfResultsSorted(self, results):
        return sorted(results)

    def str2datetime(self, dtstr):
        date, time = dtstr.split()
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)
        hour, minute = time.split(":")
        hour, minute = int(hour), int(minute)
        return datetime.datetime(year, month, day, hour, minute)

    def str2DateTime(self, dtstr):
        return DateTime(dtstr)

TESTFILES = [
    'index.rst',
    'zopeindex.rst'
]

def test_suite():

    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact,
                },
            test_class=DRIRITestcase
        ) for filename in TESTFILES])
