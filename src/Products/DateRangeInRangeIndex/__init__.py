def initialize(context):
    import index
    context.registerClass(
            index.DateRangeInRangeIndex,
            permission='Add Pluggable Index',
            constructors=(index.manage_addDRIRIndexForm,
                          index.manage_addDRIRIndex),
            icon='www/index.gif',
            visibility=None
    )