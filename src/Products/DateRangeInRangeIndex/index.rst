=====================
DateRangeInRangeIndex
=====================

--------------
Overall tests.
--------------

Lets define some dummy events and catalog them::

    (e1)   |------------------------------------------------------------------|
    (e2)                                    |---------------------------------|
    (e3)   |--------------------------------|
    (e4)   |---------------------------|

    >>> events = {
    ...     'e1': ('2000-01-01 00:00', '2000-12-31 00:00'),
    ...     'e2': ('2000-06-01 00:00', '2000-12-01 00:00'),
    ...     'e3': ('2000-01-01 00:00', '2000-06-01 00:00'),
    ...     'e4': ('2000-01-01 00:00', '2000-05-01 00:00'),
    ... }
    >>> self.dtfactory = self.str2DateTime
    >>> dummies = self.buildDummies(events)
    >>> self.catalogDummies(dummies)


Query for case 1: Both outside.
-------------------------------

Find all by defining a Date befor start of (e1) and after end of (e1|2)::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'1999-12-31 00:00','end':'2001-01-01 00:00'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e2', 'e3', 'e4']


Query for case 2: Query start inside, query end outside.
--------------------------------------------------------

::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'2000-10-01 00:00','end':'2001-01-01 00:00'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e2']


Query for case 3: Query start outside, query end inside.
--------------------------------------------------------

::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'1999-12-31 00:00','end':'2000-04-01 00:00'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e3', 'e4']


Query for case 4: Query both inside.
------------------------------------

::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'2000-10-01 00:00','end':'2000-10-31 00:00'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e2']


-----------------------
Tests on a minute level
-----------------------

Define testing data
-------------------

::

    >>> self.app.catalog.clear()

    >>> events = {
    ...     'e1': ('2000-01-01 08:15', '2000-01-01 09:30'),
    ...     'e2': ('2000-01-01 09:00', '2000-01-02 12:00'),
    ... }
    >>> dummies = self.buildDummies(events)
    >>> self.catalogDummies(dummies)

First test if we find bot by quering for the whole day 2000-01-01
from 00:00 to 23:59::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'2000-01-01 00:00','end':'2000-01-01 23:59'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e2']

Quering for the whole day 2000-01-01 from 00:01 to 23:59 might be something
different? But it shouldnt!

::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'2000-01-01 00:01','end':'2000-01-01 23:59'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e2']

So lets see if we find both by quering with a start time of 9:15 (inside both)
and a end-time outside e1 but inside e2::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'2000-01-01 09:15','end':'2000-01-01 09:59'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e1', 'e2']

If we ask for a both-inside targeting on e2 after e1 ended, only e2 must be
returned::

    >>> brains = self.app.catalog.search(
    ...     {'driri': {'start':'2000-01-01 09:31','end':'2000-01-01 09:59'} }
    ... )
    >>> self.idsOfBrainsSorted(brains)
    ['e2']

    >> self.interact(locals())
