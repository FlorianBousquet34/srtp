import socket

class RTPSessionContext:
    
    def __init__(self, packet_size: float = 32, bandwidth: float = 1e6 ) -> None:
        
        self.estimated_packet_size = packet_size
        self.session_bandwidth = bandwidth
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # The profile (context) that define the RTP Session
    
    # An estimate of the value of the average packet size
    estimated_packet_size : float
    
    # Session total bandwith for all participants in octets per seconds
    session_bandwidth: float
    
    # Fraction of bandwidth allocated to HeartBeat (RTCP / SRTCP)
    # Between 0 and 1 5% is recommanded
    control_bandwith_fraction: float = 0.05
    
    # UDP Buffer size lower than MTU
    buffer_size : int = 1400
    
    # UDP Thread waiting time
    lock_wait_time: float = 1e-3
    
    # Listenning scocket
    sock : socket.socket