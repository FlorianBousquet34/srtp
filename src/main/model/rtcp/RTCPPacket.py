from main.model.rtcp.RR.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.SR.RTCPSRPacket import RTCPSRPacket


class RTCPPacket:
    
    packet: RTCPSRPacket | RTCPRRPacket # TODO  | RTCPBYEPacket | RTPCSDESPacket | RTCPAPPPacket