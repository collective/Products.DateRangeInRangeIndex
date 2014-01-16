from zope.component import adapts

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import NodeAdapterBase
from Products.DateRangeInRangeIndex.interfaces import IDateRangeInRangeIndex

class DateRangeInRangeIndexNodeAdapter(NodeAdapterBase):
    """Node im- and exporter for DateRangeInRangeIndex.
    """

    adapts(IDateRangeInRangeIndex, ISetupEnviron)

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('index')
        node.setAttribute('startindex', self.context.startindex)
        node.setAttribute('endindex', self.context.endindex)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        _before = (self.context.startindex, self.context.endindex)
        startindex =  node.getAttribute('startindex').encode('utf-8')
	endindex = node.getAttribute('endindex').encode('utf-8')
        _after = (startindex, endindex)
        if _before != _after:
            self.context.startindex = startindex
	    self.context.endindex = endindex

    node = property(_exportNode, _importNode)

