class RTCPSimpleHeader:
    
    def to_bytes(self) -> bytearray:
        
        raw_header = bytearray(8)
        raw_header[0] = self.version * 64 + 32 * self.padding + self.block_count
        raw_header[1] = self.marker * 128 + self.payload_type
        raw_header[2:4] = self.length.to_bytes(2)
        
        return raw_header
    
    # V on 2 bits
    version: int = 2
    
    # P padding on 1 bit
    padding: bool = False
    
    marker: bool = True
    
    payload_type: int
    
    # Block number on 5 bits
    # Report blocks or SDES chuncks count
    block_count: int 
    
    #The length of this RTCP packet in 32-bit words minus one,
    # including the header and any padding
    length: int