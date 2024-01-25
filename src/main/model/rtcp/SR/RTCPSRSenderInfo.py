class RTCPSRSenderInfo:
    
    #NTP timestamp : Wallclock of 64 bits
    ntpTimestamp: int
    
    #RTP Timestamp 32 bits
    rtpTimestamp: int
    
    # 32 bits 
    # packet count sent since begining of transmission
    senderPacketCount : int
    
    # 32 bits 
    # packet size sent since beginning of transmission
    senderOctetCount : int