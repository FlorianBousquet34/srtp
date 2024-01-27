
from main.model.rtcp.RTCPPacket import RTCPPacket


class RTCPCompoundPacket:
    
    def __init__(self, raw_data) -> None:
        self.raw_data = raw_data
    
    raw_data: bytearray
    
    packets : list[RTCPPacket] = []