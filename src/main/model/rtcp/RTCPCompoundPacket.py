from main.model.rtp.RTPPacket import RTPPacket


class RTCPCompoundPacket:
    
    rawData: bytearray
    
    packets : list[RTPPacket] = []