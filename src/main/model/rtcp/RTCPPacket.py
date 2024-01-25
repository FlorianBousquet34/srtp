from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket


class RTCPPacket:
    
    packet: RTCPSRPacket | RTCPRRPacket # TODO  | RTCPBYEPacket | RTPCSDESPacket | RTCPAPPPacket