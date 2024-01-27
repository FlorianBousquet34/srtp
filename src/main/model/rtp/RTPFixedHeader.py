class RTPFixedHeader:
    
    # V on 2 bits
    version: int = 2
    
    # P padding on 1 bit
    padding: bool
    
    # X extended header on 1 bit
    extension: bool
    
    # CC number of CRSC on 4 bits
    csrc_number: int 
    
    # M marqueur on 1 bit
    marker: bool
    
    # PT on 7 bits
    # values can be provided with the RTPPaylaodTypeEnum
    # or the SRTPPayloadTypeEnum
    payload_type: int
    
    # SEQNUM on 16 bits
    sequence_number: int
    
    # timestamp on 32 bits
    timestamp: int
    
    # SSRC synchronized source on 32 bits
    ssrc: int 