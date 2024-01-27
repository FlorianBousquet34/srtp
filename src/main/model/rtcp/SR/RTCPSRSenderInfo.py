class RTCPSRSenderInfo:
    
    def to_bytes(self) -> bytearray:
        
        raw_data = bytearray(20)
        raw_data[:8] = self.ntp_timestamp.to_bytes(8)
        raw_data[8:12] = self.rtp_timestamp.to_bytes(4)
        raw_data[12:16] = self.sender_packet_count.to_bytes(4)
        raw_data[16:20] = self.sender_octet_count.to_bytes(4)
        
        return raw_data
    
    #NTP timestamp : Wallclock of 64 bits
    ntp_timestamp: int
    
    #RTP Timestamp 32 bits
    rtp_timestamp: int
    
    # 32 bits 
    # packet count sent since begining of transmission
    sender_packet_count : int
    
    # 32 bits 
    # packet size sent since beginning of transmission
    # header and padding excluded
    sender_octet_count : int