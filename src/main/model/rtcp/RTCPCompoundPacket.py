
from main.model.rtcp.RTCPPacket import RTCPPacket


class RTCPCompoundPacket:
    
    raw_data: bytearray
    
    packets : list[RTCPPacket] = []