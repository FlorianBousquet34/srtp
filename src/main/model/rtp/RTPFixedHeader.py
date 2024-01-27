class RTPFixedHeader:
    
    def to_bytes(self) -> bytearray:
        
        raw_header = bytearray(12)
        raw_header[0] = self.version * 64 + 32 * self.padding + self.extension * 16 + self.csrc_number
        raw_header[1] = self.marker * 128 + self.payload_type
        raw_header[2:4] = self.sequence_number.to_bytes(2)
        raw_header[4:8] = self.timestamp.to_bytes(4)
        raw_header[8:12] = self.ssrc.to_bytes(4)
        
        return raw_header
    
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