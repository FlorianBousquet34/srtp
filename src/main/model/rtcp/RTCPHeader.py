class RTCPHeader:
    
    marker: bool = True
    payloadType: int
    # V on 2 bits
    version: str
    
    # P padding on 1 bit
    padding: bool = False
    
    # Block number on 5 bits
    # Report blocks or SDES chuncks count
    blockCount: int 
    
    #The length of this RTCP packet in 32-bit words minus one,
    # including the header and any padding
    length: int

    # SSRC synchronized source on 32 bits
    ssrc: int 