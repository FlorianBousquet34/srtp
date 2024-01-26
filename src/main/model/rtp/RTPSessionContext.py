class RTPProfile:
    
    # The profile (context) that define the RTP Session
    
    # An estimate of the value of the average packet size
    estimated_packet_size : float
    
    # Session total bandwith for all participants in octets per seconds
    session_bandwidth: float
    
    # Fraction of bandwidth allocated to HeartBeat (RTCP / SRTCP)
    # Between 0 and 1 5% is recommanded
    control_bandwith_fraction: float = 0.05