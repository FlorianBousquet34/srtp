from main.model.rtcp.app.RTCPAPPPacket import RTCPAPPPacket
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket


class RTCPPacket:
    
    packet: RTCPSRPacket | RTCPRRPacket | RTCPBYEPacket | RTCPSDESPacket | RTCPAPPPacket
    
    raw_data: bytearray