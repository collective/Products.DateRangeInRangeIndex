Query a daterange on objects with a daterange.

Example: You want all events within a date range of next two weeks, neither if 
the event has started one week ago nor ends one week later - or both.

Consider objects with a daterange start and end. 
Use this addon to query all objects inside a query-start and query-end range, 
where either or both of objects start and end match the query range.

This index is possibly the fastest way to solve the problem, it solves it as an 
zope index and works direct with the catalogs fast IISets (or IFSets). Its much 
faster than formerly used classical catalog-query post-processing.

There are two types of indexes available: 

- ``Products.ZCatalog`` (Zope 2) compatible

- ``zope.catalog`` (Zope (3) framework) compatible

The index acts as an proxy for a more complex query on two indexes (DateIndex 
on ZCatalog or FieldIndex on zope.catalog). It utilize the other indexes and 
does not store any index-data itself.

To illustrate this a query example on ZCatalog)::

    >>> result = zcatalog.search({'myindex': {'start':'2000-10-01 00:00',
    ...                                       'end':'2010-10-31 23:59'} })

or a query example on zope.catalog::

    >>> query = catalog.apply({'myindex': (datetime(2000, 10, 01, 00, 00'), 
    ...                                    datetime(2010, 10, 31, 23, 59'))})

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

It's also possible to configure this indexer through XML. Add a
``catalog.xml`` to your profile with the following settings::

	<?xml version="1.0"?>
	<object name="portal_catalog" meta_type="Plone Catalog Tool">

    <index name="start_end_range" meta_type="DateRangeInRangeIndex">
        <startindex value="your_custom_start_field_index" />
        <endindex value="your_custom_end_field_index" />
    </index>

	</object>

The ``startindex`` and ``endindex`` nodes define the indexes for the
start and end fields of this DateRangeInRangeIndex.

Source Code
===========

The sources are in a GIT DVCS with its main branches at 
`github <http://github.com/collective/Products.DateRangeInRangeIndex>`_.

We'd be happy to see many commits, forks and pull-requests to make 
DateRangeInRangeIndex even better.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>
- Zalán Somogyváry [SyZn]
