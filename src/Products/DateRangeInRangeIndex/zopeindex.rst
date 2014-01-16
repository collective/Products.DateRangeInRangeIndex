=====================
DateRangeInRangeIndex
=====================

--------------
Overall tests.
--------------

Lets define some dummy events and catalog them::

    (1)   |------------------------------------------------------------------|
    (2)                                    |---------------------------------|
    (3)   |--------------------------------|
    (4)   |---------------------------|

    >>> events = {
    ...     1: ('2000-01-01 00:00', '2000-12-31 00:00'),
    ...     2: ('2000-06-01 00:00', '2000-12-21 00:00'),
    ...     3: ('2000-01-01 00:00', '2000-06-01 00:00'),
    ...     4: ('2000-01-01 00:00', '2000-05-01 00:00'),
    ... }
    >>> import datetime
    >>> self.dtfactory = self.str2datetime
    >>> dummies = self.buildDummies(events)
    >>> self.z3catalogDummies(dummies)


Query for case 1: Both outside.
-------------------------------

Find all by defining a Date befor start of (e1) and after end of (e1|2)::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('1999-12-31 00:00'), 
    ...                self.str2datetime('2001-01-01 00:00')) }
    ... )
    
    >>> self.idsOfResultsSorted(results)
    [1, 2, 3, 4]
    


Query for case 2: Query start inside, query end outside.
--------------------------------------------------------

::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('2000-10-01 00:00'), 
    ...                self.str2datetime('2001-01-01 00:00')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [1, 2]


Query for case 3: Query start outside, query end inside.
--------------------------------------------------------

::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('1999-12-31 00:00'), 
    ...                self.str2datetime('2000-04-01 00:00')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [1, 3, 4]


Query for case 4: Query both inside.
------------------------------------

::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('2000-10-01 00:00'), 
    ...                self.str2datetime('2000-10-31 00:00')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [1, 2]


-----------------------
Tests on a minute level
-----------------------

Define testing data
-------------------

::

    >>> self.app.z3catalog.clear()

    >>> events = {
    ...     1: ('2000-01-01 08:15', '2000-01-01 09:30'),
    ...     2: ('2000-01-01 09:00', '2000-01-02 12:00'),
    ... }
    >>> dummies = self.buildDummies(events)
    >>> self.z3catalogDummies(dummies)

First test if we find bot by quering for the whole day 2000-01-01
from 00:00 to 23:59::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('2000-01-01 00:00'), 
    ...                self.str2datetime('2000-01-01 23:59')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [1, 2]

Quering for the whole day 2000-01-01 from 00:01 to 23:59 might be something
different? But it shouldnt!

::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('2000-01-01 00:01'), 
    ...                self.str2datetime('2000-01-01 23:59')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [1, 2]

So lets see if we find both by quering with a start time of 9:15 (inside both)
and a end-time outside e1 but inside e2::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('2000-01-01 09:15'), 
    ...                self.str2datetime('2000-01-01 09:59')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [1, 2]

If we ask for a both-inside targeting on e2 after e1 ended, only e2 must be
returned::

    >>> results = self.app.z3catalog.apply(
    ...     {'driri': (self.str2datetime('2000-01-01 09:31'), 
    ...                self.str2datetime('2000-01-01 09:59')) }
    ... )
    >>> self.idsOfResultsSorted(results)
    [2]

    >> self.interact(locals())
