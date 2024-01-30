from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.srtcp.SRTCPPacket import SRTCPPacket


class SRTCPCompoundPacket(RTCPCompoundPacket):

    packets : list[SRTCPPacket] = []
    