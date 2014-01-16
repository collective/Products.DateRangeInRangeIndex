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
        child_start = self._doc.createElement('startindex')
        child_start.attributes["value"] = self.context.startindex
        child_end = self._doc.createElement('endindex')
        child_end.attributes["value"] = self.context.endindex
        node.appendChild(child_start)
        node.appendChild(child_end)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        child_nodes = {_.tagName:_.getAttribute('value') for _ in node.childNodes if _.nodeType==1}
        self.context.startindex = child_nodes["startindex"].encode('utf-8')
        self.context.endindex = child_nodes["endindex"].encode('utf-8')

    node = property(_exportNode, _importNode)

