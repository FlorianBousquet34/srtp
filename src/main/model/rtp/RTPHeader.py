from main.model.rtp.RTPFixedHeader import RTPFixedHeader
from main.model.rtp.RTPHeaderExtension import RTPHeaderExtension


class RTPHeader:
    
    # The fixed length part of the header
    fixedHeader: RTPFixedHeader
    
    # Enable the header extension implementations
    headerExtesion: RTPHeaderExtension
    
    # The list of constribution source (CSRC)
    # from 0 up to 15 items of 32 bits identifier
    csrcList: list[int]