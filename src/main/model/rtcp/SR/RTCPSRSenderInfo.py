class RTCPSRSenderInfo:
    
    #NTP timestamp : Wallclock of 64 bits
    ntp_timestamp: int
    
    #RTP Timestamp 32 bits
    rtp_timestamp: int
    
    # 32 bits 
    # packet count sent since begining of transmission
    sender_packet_count : int
    
    # 32 bits 
    # packet size sent since beginning of transmission
    sender_octet_count : int