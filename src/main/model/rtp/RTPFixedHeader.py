from datetime import datetime

class RTPFixedHeader:
    
    # V on 2 bits
    version: str
    
    # P padding on 1 bit
    padding: bool
    
    # X extended header on 1 bit
    extension: bool
    
    # CC number of CRSC on 4 bits
    csrcNumber: int 
    
    # M marqueur on 1 bit
    marker: bool
    
    # PT on 7 bits
    # values can be provided with the RTPPaylaodTypeEnum
    # or the SRTPPayloadTypeEnum
    payloadType: int
    
    # SEQNUM on 16 bits
    sequenceNumber: int
    
    # datetime on 32 bits
    timestamp: datetime
    
    # SSRC synchronized source on 32 bits
    synchSource: int 