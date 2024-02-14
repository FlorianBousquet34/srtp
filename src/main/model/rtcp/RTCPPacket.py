from src.main.model.rtcp.app.RTCPAPPPacket import RTCPAPPPacket
from src.main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from src.main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from src.main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from src.main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket


class RTCPPacket:
    
    def __init__(self, packet : RTCPSRPacket | RTCPRRPacket | RTCPBYEPacket | RTCPSDESPacket | RTCPAPPPacket = None) -> None:
        
        self.packet = packet
        
    packet: RTCPSRPacket | RTCPRRPacket | RTCPBYEPacket | RTCPSDESPacket | RTCPAPPPacket
    
    raw_data: bytearray
    
    def to_bytes(self) -> bytearray:
        
        self.raw_data = self.packet.to_bytes()
        
        # compute length
        self.packet.header.length = len(self.raw_data) // 4 - 1
        
        self.raw_data[2:4] = self.packet.header.length.to_bytes(2)
        
        return self.raw_data