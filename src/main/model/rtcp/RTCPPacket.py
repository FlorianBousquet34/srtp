from main.model.rtcp.app.RTCPAPPPacket import RTCPAPPPacket
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket


class RTCPPacket:
    
    packet: RTCPSRPacket | RTCPRRPacket | RTCPBYEPacket | RTCPSDESPacket | RTCPAPPPacket
    
    raw_data: bytearray
    
    def to_bytes(self) -> bytearray:
        
        self.raw_data = self.packet.to_bytes()
        
        # compute length
        self.packet.header.length = len(self.raw_data) // 4 - 1
        
        self.raw_data[2:4] = self.packet.header.length.to_bytes(2)
        
        return self.raw_data