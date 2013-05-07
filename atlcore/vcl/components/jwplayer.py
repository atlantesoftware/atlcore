#encoding=UTF-8

from atlcore.vcl.components.component import Component
from atlcore.vcl.exceptions import ComponentVersionError

class JWPlayer(object):
    
    def __new__(self, data_provider=None, version=None):
        if version:
            if version == '5.1.854':
                from atlcore.vcl.components import jwplayer_v5_1_854
                return jwplayer_v5_1_854.JWPlayer(data_provider)
            elif version == '5.6.1768':
                from atlcore.vcl.components import jwplayer_v5_6_1768
                return jwplayer_v5_6_1768.JWPlayer(data_provider, version)
            elif version == '5.8':
                from atlcore.vcl.components import jwplayer_v5_8
                return jwplayer_v5_8.JWPlayer(data_provider)
            else:
                raise ComponentVersionError()
        else:
            from atlcore.vcl.components.jwplayer_v5_8 import JWPlayer as JWPlayer_v
            return JWPlayer_v(data_provider)
