Finds all objects with some date range (two dates) - such as an event start and
end - inside the date range of a query-start and query-end.

Example: You want all events within a date range of next two weeks, neither if 
the event has started one week ago nor ends one week later - or both.

This index is possibly the fastest way to solve the problem, it solves it as an 
Zope index and works direct with the catalogs fast IISets. Its much faster than 
classical catalog-query post-processing.

The index acts as an proxy for a more complex query on two DateIndexes. It 
utilize the other indexes and does not store any index-data itself.

Query Example::

    TODO


Source Code
===========

The sources are in a GIT DVCS with its main branches at 
`github <http://github.com/collective/Products.DateRangeInRangeIndex>`_.

We'd be happy to see many commits, forks and pull-requests to make 
DateRangeInRangeIndex even better.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

