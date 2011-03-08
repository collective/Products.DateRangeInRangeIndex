Finds all objects with some date range (two dates) - such as an event start and
end - inside the date range of a query-start and query-end.

Example: You want all events within a date range of next two weeks, neither if 
the event has started one week ago nor ends one week later - or both.

This index is possibly the fastest way to solve the problem, it solves it as an 
Zope index and works direct with the catalogs fast IISets. Its much faster than 
classical catalog-query post-processing.

The index acts as an proxy for a more complex query on two DateIndexes. It 
utilize the other indexes and does not store any index-data itself.

To illustrate this a query example::

    {'myindex': {'start':'2000-10-01 00:00','end':'2010-10-31 23:59'} }

This will find objects (consider start is always before end date): 

1) where start date is before 2000-10-01 and end date is after 2010-10-31.
2) where start date is between 2000-10-01 and 2010-10-31.
3) where end date is between 2000-10-01 and 2010-10-31.
4) where both are between 2000-10-01 and 2010-10-31.

ASCII-Art of the above (q=query, e=event)::
            
     Q)    q_start|--------------------|q_end
     
     1) e_start|---------------------------|e_end
    
     2) e_start|---------------|e_end
     
     3)           e_start|-----------------|e_end
    
     4)           e_start|-----|e_end
 

Source Code
===========

The sources are in a GIT DVCS with its main branches at 
`github <http://github.com/collective/Products.DateRangeInRangeIndex>`_.

We'd be happy to see many commits, forks and pull-requests to make 
DateRangeInRangeIndex even better.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

