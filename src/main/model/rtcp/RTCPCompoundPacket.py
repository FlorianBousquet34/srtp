
from main.model.rtcp.RTCPPacket import RTCPPacket


class RTCPCompoundPacket:
    
    rawData: bytearray
    
    packets : list[RTCPPacket] = []