
History
=======

2.0.3 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- *add item here*

Bug fixes:

- *add item here*


2.0.2 (2025-02-28)
------------------

- Fix Exception when calling ``catalog.getIndexDataForRID(rid)`` by implementing
  missing ``getEntryForObject`` method
  [petschki]


2.0.1 (2019-03-21)
------------------

- Fix exportimport.py (GenericSetup) for Python 3 and add Python 3.7 to test matrix
  [MrTango]


2.0 (2018-07-12)
----------------

- Add support for ``Products.ZCatalog >= 4`` while dropping support for older
  versions. [icemac, 2018-07-11]

- Add support for Python 3.5 and Python 3.6 on Zope 4. While dropping support
  for older Zope versions. [icemac, 2018-07-11]

- Remove dependency from `Globals` for Zope 4 compat. [sallner, 2017-08-21]

- some code cleanup [jensens, 2016-06-14]

1.3
---

- added support for generic setup [SyZn, 2014-01-16]

1.2
---

- added zope.catalog compatible index. [jensens, 2012-04-12]

1.1
---

- eggification and release at pypi [jensens, 2011-03-08]

1.0
---

-  final release as Zope Product [jensens, 2007-08-29]

