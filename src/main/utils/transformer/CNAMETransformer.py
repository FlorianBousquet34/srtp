from typing import Tuple


class CNAMETransformer:
    
    @staticmethod
    def transform_cname(cname: str) -> Tuple[str, int]:
        # !!! Override this method for other cname formats
        # parsing of cname that should be formated 'user@host:port'
        # or host:port
        
        split : list
        if '@' in cname:
            split = cname.split('@')[1].split(':')
        else:
            split = cname.split(':')
        
        return split[0], int(split[1])