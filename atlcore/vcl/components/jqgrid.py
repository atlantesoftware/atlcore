#encoding=UTF-8
from atlcore.vcl.exceptions import ComponentVersionError

class JQGrid(object):
    
    def __new__(self, data_provider, version=None):
        if version:
            if version == '4.0.0':
                from atlcore.vcl.components.jqgrid_v4_0_0 import JQGrid_v4_0_0 
                return JQGrid_v4_0_0(data_provider)
            elif version == '3.8.2':
                from atlcore.vcl.components.jqgrid_v3_8_2 import JQGrid_v3_8_2 
                return JQGrid_v3_8_2(data_provider)
            else:
                raise ComponentVersionError()
        else:
            from atlcore.vcl.components.jqgrid_v4_0_0 import JQGrid_v4_0_0 
            return JQGrid_v4_0_0(data_provider)