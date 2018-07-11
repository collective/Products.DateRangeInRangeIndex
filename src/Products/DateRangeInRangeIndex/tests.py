# -*- coding: utf-8 -*-
from DateTime import DateTime
from interlude import interact
from Products.DateRangeInRangeIndex.index import DateRangeInRangeIndex as z2DateRangeInRangeIndex  # noqa
from Products.DateRangeInRangeIndex.zopeindex import DateRangeInRangeIndex as z3DateRangeInRangeIndex  # noqa
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex
from Products.ZCatalog.Catalog import Catalog as z2Catalog
from Testing import ZopeTestCase as ztc
from zope.catalog.catalog import Catalog as z3Catalog
from zope.catalog.field import FieldIndex

import datetime
import doctest
import unittest

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
        """Set up a base scenario."""
        # Zope 2 Index bootstrap
        self.app.catalog = z2Catalog()
        idxstart = DateIndex('start')
        idxend = DateIndex('end')
        self.app.catalog.addIndex('start', idxstart)
        self.app.catalog.addIndex('end', idxend)
        driri = z2DateRangeInRangeIndex(
            'driri',
            extra={
                'startindex': 'start',
                'endindex': 'end'
            },
            caller=self.app.catalog
        )
        self.app.catalog.addIndex('driri', driri)
        self.app.catalog.addColumn('id')

        # Zope 3 Index bootstrap
        self.app.z3catalog = z3Catalog()
        self.app.z3catalog[u'start'] = FieldIndex(
            field_name='start',
            field_callable=False
        )
        self.app.z3catalog[u'end'] = FieldIndex(
            field_name='end',
            field_callable=False
        )
        self.app.z3catalog[u'driri'] = z3DateRangeInRangeIndex(
            u'start',
            u'end'
        )

    def buildDummies(self, cases):
        """setup dummies"""
        dummies = {}
        for id in cases:
            dummy = DummyEvent(
                id,
                self.dtfactory(cases[id][0]),
                self.dtfactory(cases[id][1])
            )
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


class IndexTests(DRIRITestcase):
    """Tests of .index.DateRangeInRangeIndex. to increase test coverage."""

    def test_index__DateRangeInRangeIndex____init____1(self):
        """It can be called without an `extra`."""
        index = z2DateRangeInRangeIndex('driri')
        self.assertIsNone(index.startindex)
        self.assertIsNone(index.endindex)

    def test_index__DateRangeInRangeIndex____init____2(self):
        """The `extra` can have the configuration on attributes."""
        class extra:
            startindex = 'start'
            endindex = 'end'
        index = z2DateRangeInRangeIndex('driri', extra=extra)
        self.assertEqual('start', index.startindex)
        self.assertEqual('end', index.endindex)

    def test_index__DateRangeInRangeIndex____init____3(self):
        """It raises a ValueError if `extra` has not the needed keys."""
        with self.assertRaises(ValueError) as err:
            z2DateRangeInRangeIndex('driri', extra={})
        self.assertTrue(str(err.exception).startswith(
            "DateRangeInRangeIndex needs 'extra' kwarg with keys or "))

    def test_index__DateRangeInRangeIndex__query_index__1(self):
        """It requires a `caller` to be set."""
        index = z2DateRangeInRangeIndex(
            'driri', extra={'startindex': 'start', 'endindex': 'end'})
        with self.assertRaises(ValueError) as err:
            index.query_index({'start': 1, 'end': 2})
        self.assertEqual(
            'DateRangeInRangeIndex cant work w/o knowing about its catalog',
            str(err.exception))


TESTFILES = [
    'index.rst',
    'zopeindex.rst'
]


def test_suite():

    suite = unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact},
            test_class=DRIRITestcase
        ) for filename in TESTFILES])
    suite.addTests(unittest.makeSuite(IndexTests))
    return suite
